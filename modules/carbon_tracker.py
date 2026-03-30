"""
Terra 2.0 — Carbon Footprint Tracker
Calculates emissions across transport, food, energy, and shopping categories.
Generates PDF reports with ReportLab.
"""

from datetime import datetime
from io import BytesIO
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from sqlalchemy import select

from config import (
    TRANSPORT_FACTORS, FOOD_FACTORS, ENERGY_FACTOR_INDIA,
    SHOPPING_FACTORS, INDIA_AVG_DAILY_KG, REPORTS_DIR
)
from database.db_setup import get_engine, get_session, FootprintLog


class CarbonTracker:
    """Calculates carbon emissions and generates reports."""

    @staticmethod
    def calculate_transport(mode: str, km: float) -> float:
        """Calculate transport CO2 in kg for given mode and distance."""
        factor = TRANSPORT_FACTORS.get(mode, 0.0)
        return round(factor * km, 3)

    @staticmethod
    def calculate_food(diet_type: str, meals: int) -> float:
        """Calculate food CO2 in kg for a given diet type and number of meals."""
        daily_factor = FOOD_FACTORS.get(diet_type, 3.81)
        per_meal = daily_factor / 3.0
        return round(per_meal * meals, 3)

    @staticmethod
    def calculate_energy(kwh_per_day: float) -> float:
        """Calculate energy CO2 in kg from kWh consumed."""
        return round(kwh_per_day * ENERGY_FACTOR_INDIA, 3)

    @staticmethod
    def calculate_shopping(items_dict: dict) -> float:
        """
        Calculate shopping CO2 from dict of items.
        items_dict = {"Clothing item": 2, "Electronic device": 1}
        """
        total = 0.0
        for item_name, quantity in items_dict.items():
            factor = SHOPPING_FACTORS.get(item_name, 0.0)
            total += factor * quantity
        return round(total, 3)

    @staticmethod
    def get_total(transport: float, food: float,
                  energy: float, shopping: float) -> dict:
        """
        Get total emissions with all categories, comparison, and rating.
        """
        total = round(transport + food + energy + shopping, 3)

        if total < 3.5:
            rating = "Low"
            rating_color = "#22C55E"
            rating_emoji = "🌿"
        elif total < 7.0:
            rating = "Average"
            rating_color = "#F59E0B"
            rating_emoji = "⚡"
        else:
            rating = "High"
            rating_color = "#EF4444"
            rating_emoji = "🔥"

        comparison_pct = round((total / INDIA_AVG_DAILY_KG) * 100, 1)

        return {
            "transport_kg": transport,
            "food_kg": food,
            "energy_kg": energy,
            "shopping_kg": shopping,
            "total_kg": total,
            "rating": rating,
            "rating_color": rating_color,
            "rating_emoji": rating_emoji,
            "india_avg": INDIA_AVG_DAILY_KG,
            "comparison_pct": comparison_pct,
            "comparison_text": (
                f"Your footprint is {comparison_pct}% of the India average "
                f"({INDIA_AVG_DAILY_KG} kg/day)"
            ),
        }

    @staticmethod
    def generate_tips(results: dict) -> list:
        """Generate 5 personalized tips based on highest category."""
        tips = []

        categories = {
            "transport_kg": results.get("transport_kg", 0),
            "food_kg": results.get("food_kg", 0),
            "energy_kg": results.get("energy_kg", 0),
            "shopping_kg": results.get("shopping_kg", 0),
        }

        sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        highest = sorted_cats[0][0] if sorted_cats else "transport_kg"

        transport_tips = [
            "🚌 Switch to public transport — saves up to 2.5 kg CO2 per trip",
            "🚲 Cycle or walk for trips under 3 km — zero emissions!",
            "🚘 Carpool with friends — 4 people = 75% fewer emissions",
            "🚇 Take the metro/train — 5x less CO2 than driving",
            "🏠 Work from home one day a week — saves 20% commute emissions",
        ]

        food_tips = [
            "🥗 Try Meatless Mondays — one day saves 6.5 kg CO2/week",
            "🥕 Eat seasonal local produce — cuts food miles by 50%",
            "🌱 Swap one meat meal for plant-based daily — saves 2.5 kg CO2",
            "🍳 Choose eggs over meat — 4x lower carbon footprint",
            "🧊 Reduce food waste — composting saves methane emissions",
        ]

        energy_tips = [
            "❄️ Set AC to 24°C instead of 18°C — uses 3x less energy",
            "💡 Switch to LED bulbs — 75% less energy, last 25x longer",
            "🔌 Unplug chargers when not in use — saves 100 kWh/year",
            "☀️ Dry clothes on a line — saves 2.4 kg CO2 per load",
            "🌡️ Use a fan + AC combo — reduces AC runtime by 30%",
        ]

        shopping_tips = [
            "♻️ Buy second-hand electronics — extends product life 2+ years",
            "👗 Choose quality over quantity — 1 good item > 5 fast fashion",
            "📦 Avoid excessive packaging — carries hidden carbon costs",
            "🔧 Repair before replacing — saves manufacturing emissions",
            "🌿 Support sustainable brands — vote with your wallet",
        ]

        tip_map = {
            "transport_kg": transport_tips,
            "food_kg": food_tips,
            "energy_kg": energy_tips,
            "shopping_kg": shopping_tips,
        }

        # Add 3 tips from highest category and 1 each from next two
        primary_tips = tip_map.get(highest, transport_tips)
        tips.extend(primary_tips[:3])

        for cat_name, _ in sorted_cats[1:3]:
            cat_tips = tip_map.get(cat_name, transport_tips)
            if cat_tips:
                tips.append(cat_tips[0])

        if len(tips) < 5:
            remaining = 5 - len(tips)
            for cat_name, _ in sorted_cats:
                cat_tips = tip_map.get(cat_name, [])
                for t in cat_tips:
                    if t not in tips and len(tips) < 5:
                        tips.append(t)

        return tips[:5]

    @staticmethod
    def save_log(user_id: int, results: dict) -> bool:
        """Save footprint log to database."""
        engine = get_engine()
        try:
            with get_session(engine) as session:
                log = FootprintLog(
                    user_id=user_id,
                    date=datetime.utcnow(),
                    transport_kg=results.get("transport_kg", 0.0),
                    food_kg=results.get("food_kg", 0.0),
                    energy_kg=results.get("energy_kg", 0.0),
                    shopping_kg=results.get("shopping_kg", 0.0),
                    total_kg=results.get("total_kg", 0.0),
                    created_at=datetime.utcnow(),
                )
                session.add(log)
                session.commit()
                return True
        except Exception:
            return False

    @staticmethod
    def get_history(user_id: int) -> pd.DataFrame:
        """
        Get footprint history as DataFrame.
        Columns: date, total_kg, transport_kg, food_kg, energy_kg, shopping_kg
        """
        engine = get_engine()
        with get_session(engine) as session:
            logs = session.execute(
                select(FootprintLog)
                .where(FootprintLog.user_id == user_id)
                .order_by(FootprintLog.date.desc())
            ).scalars().all()

            if not logs:
                return pd.DataFrame(columns=[
                    "date", "total_kg", "transport_kg",
                    "food_kg", "energy_kg", "shopping_kg"
                ])

            data = []
            for log in logs:
                data.append({
                    "date": log.date.strftime("%Y-%m-%d") if log.date else "",
                    "total_kg": log.total_kg,
                    "transport_kg": log.transport_kg,
                    "food_kg": log.food_kg,
                    "energy_kg": log.energy_kg,
                    "shopping_kg": log.shopping_kg,
                })

            return pd.DataFrame(data)

    @staticmethod
    def generate_pdf_report(user_name: str, results: dict) -> Path:
        """
        Generate branded Terra 2.0 PDF report.
        Returns Path to the generated PDF.
        """
        file_path = REPORTS_DIR / f"{user_name}_report.pdf"

        doc = SimpleDocTemplate(
            str(file_path),
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "TerraTitle",
            parent=styles["Title"],
            fontSize=28,
            textColor=colors.HexColor("#2ECC71"),
            spaceAfter=6,
        )

        subtitle_style = ParagraphStyle(
            "TerraSubtitle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=colors.HexColor("#7EC8E3"),
            spaceAfter=20,
        )

        heading_style = ParagraphStyle(
            "TerraHeading",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#2ECC71"),
            spaceAfter=10,
            spaceBefore=20,
        )

        normal_style = ParagraphStyle(
            "TerraNormal",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#333333"),
            spaceAfter=6,
        )

        elements = []

        # Header
        elements.append(Paragraph("🌍 Terra 2.0", title_style))
        elements.append(Paragraph(
            "Your planet needs a glow-up. Start here.", subtitle_style
        ))
        elements.append(Spacer(1, 12))

        # Report info
        now = datetime.now()
        elements.append(Paragraph(
            f"<b>Report for:</b> {user_name}", normal_style
        ))
        elements.append(Paragraph(
            f"<b>Date:</b> {now.strftime('%B %d, %Y at %I:%M %p')}", normal_style
        ))
        elements.append(Spacer(1, 20))

        # Score table
        elements.append(Paragraph("📊 Carbon Footprint Breakdown", heading_style))

        table_data = [
            ["Category", "Emissions (kg CO2)", "Percentage"],
            [
                "🚗 Transport",
                f"{results.get('transport_kg', 0):.2f}",
                f"{(results.get('transport_kg', 0) / max(results.get('total_kg', 1), 0.01) * 100):.1f}%"
            ],
            [
                "🍽️ Food",
                f"{results.get('food_kg', 0):.2f}",
                f"{(results.get('food_kg', 0) / max(results.get('total_kg', 1), 0.01) * 100):.1f}%"
            ],
            [
                "⚡ Energy",
                f"{results.get('energy_kg', 0):.2f}",
                f"{(results.get('energy_kg', 0) / max(results.get('total_kg', 1), 0.01) * 100):.1f}%"
            ],
            [
                "🛍️ Shopping",
                f"{results.get('shopping_kg', 0):.2f}",
                f"{(results.get('shopping_kg', 0) / max(results.get('total_kg', 1), 0.01) * 100):.1f}%"
            ],
            [
                "TOTAL",
                f"{results.get('total_kg', 0):.2f}",
                "100%"
            ],
        ]

        table = Table(table_data, colWidths=[200, 150, 100])

        # Rating color for total row
        rating = results.get("rating", "Average")
        if rating == "Low":
            total_color = colors.HexColor("#22C55E")
        elif rating == "Average":
            total_color = colors.HexColor("#F59E0B")
        else:
            total_color = colors.HexColor("#EF4444")

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2ECC71")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -2), colors.HexColor("#F5F5F5")),
            ("BACKGROUND", (0, -1), (-1, -1), total_color),
            ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#DDDDDD")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -2), [
                colors.white, colors.HexColor("#F9F9F9")
            ]),
            ("TOPPADDING", (0, 1), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        # Rating
        elements.append(Paragraph(
            f"📈 Rating: <b>{results.get('rating_emoji', '')} "
            f"{results.get('rating', 'N/A')}</b>",
            heading_style
        ))
        elements.append(Paragraph(
            results.get("comparison_text", ""), normal_style
        ))
        elements.append(Spacer(1, 10))

        # India average comparison
        elements.append(Paragraph(
            f"🇮🇳 India daily average: <b>{INDIA_AVG_DAILY_KG} kg CO2</b>",
            normal_style
        ))
        elements.append(Paragraph(
            f"📊 Your footprint: <b>{results.get('comparison_pct', 0)}%</b> "
            f"of India average",
            normal_style
        ))
        elements.append(Spacer(1, 20))

        # Bar chart
        elements.append(Paragraph("📊 Emissions Breakdown Chart", heading_style))

        drawing = Drawing(400, 200)
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 30
        chart.width = 300
        chart.height = 140
        chart.data = [[
            results.get("transport_kg", 0),
            results.get("food_kg", 0),
            results.get("energy_kg", 0),
            results.get("shopping_kg", 0),
        ]]
        chart.categoryAxis.categoryNames = [
            "Transport", "Food", "Energy", "Shopping"
        ]
        chart.categoryAxis.labels.angle = 0
        chart.categoryAxis.labels.fontSize = 9
        chart.valueAxis.valueMin = 0
        chart.valueAxis.labels.fontSize = 8
        chart.bars[0].fillColor = colors.HexColor("#2ECC71")
        chart.bars[0].strokeColor = colors.HexColor("#1a9c54")
        chart.barWidth = 40
        drawing.add(chart)
        elements.append(drawing)
        elements.append(Spacer(1, 20))

        # Tips
        tips = CarbonTracker.generate_tips(results)
        elements.append(Paragraph("💡 Personalised Tips", heading_style))
        for i, tip in enumerate(tips, 1):
            elements.append(Paragraph(f"{i}. {tip}", normal_style))

        elements.append(Spacer(1, 30))

        # Footer
        footer_style = ParagraphStyle(
            "TerraFooter",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#999999"),
            alignment=1,
        )
        elements.append(Paragraph(
            "Generated by Terra 2.0 🌍 — Your planet needs a glow-up.",
            footer_style
        ))

        doc.build(elements)
        return file_path
