from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Receipt:
    date: datetime
    merchant: str
    total: float
    items: List[str]
    tax: Optional[float] = None
    payment_method: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Receipt":
        """Create a Receipt instance from a dictionary."""
        # Convert date string to datetime if needed
        if isinstance(data.get("date"), str):
            try:
                date = datetime.strptime(data["date"], "%m/%d")
                # Set year to current year if not provided
                date = date.replace(year=datetime.now().year)
            except ValueError:
                date = datetime.now()
        else:
            date = data.get("date", datetime.now())

        # Convert total to float if it's a string
        total = float(data.get("total_amount", 0))
        if isinstance(total, str):
            total = float(total.replace("$", "").replace(",", ""))

        # Handle items list
        items = []
        if isinstance(data.get("items_purchased"), list):
            for item in data["items_purchased"]:
                if isinstance(item, dict):
                    items.append(
                        f"{item.get('name', 'Unknown')} - ${item.get('price', 0):.2f}"
                    )
                elif isinstance(item, str):
                    items.append(item)
        elif isinstance(data.get("items"), str):
            items = [item.strip() for item in data["items"].split(",") if item.strip()]

        # Convert tax to float if it exists
        tax = data.get("tax_amount")
        if tax is not None:
            try:
                tax = float(tax)
            except (ValueError, TypeError):
                tax = None

        return cls(
            date=date,
            merchant=data.get("merchant_name", "Unknown"),
            total=total,
            items=items,
            tax=tax,
            payment_method=data.get("payment_method"),
        )

    def to_row(self) -> List[str]:
        """Convert receipt to a row format for Google Sheets."""
        return [
            self.date.strftime("%Y-%m-%d"),
            self.merchant,
            f"${self.total:.2f}",
            ", ".join(self.items),
            f"${self.tax:.2f}" if self.tax else "",
            self.payment_method or "",
        ]
