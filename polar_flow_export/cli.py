import typer
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Annotated

from polar_flow_export.polarflowexport import export_data
from polar_flow_export.utils.date import date_trunc

app = typer.Typer()


class TyperDate:
    """A date formatted YYYY-mm-dd"""
    def __init__(self, value: date):
        self.value = value

    def __str__(self):
        return self.value.strftime("%Y-%m-%d")


def parse_typer_date(value: str) -> TyperDate:
    if isinstance(value, TyperDate):
        return value
    dt = datetime.strptime(value, "%Y-%m-%d")
    d = date_trunc(dt)
    return TyperDate(d)


@app.command()
def export(
    email: Annotated[str, typer.Argument(help="The email as used to login for Polar flow website.")],
    password: Annotated[str, typer.Argument(help="The password used to login for Polar flow website. Make sure that if"
                                                 " you use special characters that you surround it with single quotes"
                                                 " and escape single quotes that are part of the password.")],
    from_day: Annotated[
        TyperDate,
        typer.Option(
            help="The start of the timeframe for which to export data (ISO-8601 formatted YYYY-mm-dd).",
            parser=parse_typer_date
        )
    ] = TyperDate(date_trunc(datetime.now() - timedelta(days=31))),
    to_day: Annotated[
        TyperDate,
        typer.Option(
            help="The end of the timeframe for which to export data (ISO-8601 formatted YYYY-mm-dd).",
            parser=parse_typer_date
        )
    ] = TyperDate(date_trunc(datetime.now())),
    output_dir: Annotated[
        Path,
        typer.Argument(help="An existing directory in which the exported data should be stored.", exists=True,
                       file_okay=False)
    ] = Path(".")
) -> None:
    """
    Export training and/or fitness data from Polar flow website. By default it exports the last 31 days.
    """
    export_data(
        email=email,
        password=password,
        from_date=str(from_day),
        to_date=str(to_day),
        output_dir=output_dir
    )


if __name__ == "__main__":
    app()
