from dataclasses import dataclass, field


@dataclass
class ExplanationItem:

    # Nombre de la dimensión

    name: str

    # Score normalizado (0-1)

    score: float


@dataclass
class Explanation:

    # Nombre del bloque

    title: str

    # Score agregado

    score: float

    # Explicación detallada

    items: list[ExplanationItem] = field(default_factory=list)

    def lines(self) -> list[str]:

        lines = []

        lines.append(
            f"{self.title} ({self.score:.1%})"
        )

        for item in self.items:

            lines.append(
                f"   - {item.name:<12} {item.score:6.1%}"
            )

        return lines