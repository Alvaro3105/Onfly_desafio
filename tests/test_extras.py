"""Testes adicionais: cenários não cobertos pelos testes fornecidos."""

from helpers import run_cli


def test_top_hotels_tie_breaks_by_hotel_id(tmp_path):
    """Empate em total_brl: desempata por hotel_id crescente."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "hotel_id": "H03", "amount": "500.00"},
            {"reservation_id": "R-2", "hotel_id": "H01", "amount": "500.00"},
            {"reservation_id": "R-3", "hotel_id": "H02", "amount": "500.00"},
        ],
    )
    assert [h["hotel_id"] for h in report["top_hotels"]] == ["H01", "H02", "H03"]


def test_no_show_and_cancelled_excluded_from_totals(tmp_path):
    """NO_SHOW e CANCELLED contam nas reservas, mas não em noites nem valores."""
    report = run_cli(
        tmp_path,
        [
            {"reservation_id": "R-1", "status": "CONFIRMED", "amount": "100.00"},
            {"reservation_id": "R-2", "status": "NO_SHOW", "amount": "999.00"},
            {"reservation_id": "R-3", "status": "CANCELLED", "amount": "999.00"},
        ],
    )
    summary = report["summary"]
    assert summary["total_reservations"] == 3
    assert summary["confirmed_reservations"] == 1
    assert summary["no_show_reservations"] == 1
    assert summary["cancelled_reservations"] == 1
    assert summary["total_room_nights"] == 1
    assert summary["total_amount_brl"] == "100.00"


def test_nights_across_year_boundary(tmp_path):
    """Virada de ano: 30/12 a 02/01 com 2 quartos = 6 noites, no mês do check-in."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-12-30",
                "checkout_date": "2026-01-02",
                "rooms": "2",
            }
        ],
    )
    assert report["summary"]["total_room_nights"] == 6
    assert report["by_month"][0]["month"] == "2025-12"


def test_reads_more_than_200_rows(tmp_path):
    """Todas as linhas do arquivo são lidas, sem limite fixo."""
    rows = [{"reservation_id": f"R-{i}"} for i in range(250)]
    report = run_cli(tmp_path, rows)
    assert report["summary"]["total_reservations"] == 250


def test_currency_conversion_uses_decimal(tmp_path):
    """USD 0.10 x 5.42 = 0.542, arredondado half-up para 0.54."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": "R-1", "currency": "USD", "amount": "0.10"}],
    )
    assert report["summary"]["total_amount_brl"] == "0.54"
