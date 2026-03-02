from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple

@dataclass
class TLE:
    name: str
    sat_num: int
    elset_class: str
    int_designator: str
    epoch_utc: float
    epoch_year: int
    epoch_day: float
    n_dot: float
    n_ddot: float
    bstar: float
    elem_set_type: int
    elem_number: int
    inc: float
    raan: float
    ecc: float
    argp: float
    M: float
    n: float
    rev_num: int

    line1: str
    line2: str

    @staticmethod
    def _parse_exponential(field: str) -> float:
        """
        Parses TLE compact exponent format:
            " 34123-4" -> 0.34123e-4
            "-12345-5" -> -0.12345e-5
            " 00000-0" -> 0
        """
        clean_field = field.strip()
        if not clean_field:
            return 0.0

        # Determine overall sign of the number
        sign = -1.0 if clean_field.startswith("-") else 1.0
        unsigned_field = clean_field.lstrip("+-")

        # Extract exponent (last two characters: sign + digit)
        exponent_sign = -1 if unsigned_field[-2] == "-" else 1
        exponent_value = exponent_sign * int(unsigned_field[-1])

        # Extract mantissa (everything except last two chars)
        mantissa_digits = unsigned_field[:-2].strip()
        mantissa_value = (
            float("0." + mantissa_digits)
            if mantissa_digits.strip("0")
            else 0.0
        )

        return sign * mantissa_value * (10 ** exponent_value)

    @staticmethod
    def _extract_from_text(tle_text: str) -> Tuple[str, str, str]:
        """
        Extracts (name, line1, line2) from raw TLE text.

        Supports:
            - 3-line format: name, line1, line2
            - 2-line format: line1, line2 (name="")
        """
        # Remove empty lines and trailing whitespace
        lines = [ln.rstrip() for ln in tle_text.splitlines() if ln.strip()]

        # Case 1: 3-line format (name + line1 + line2)
        if len(lines) >= 3 and lines[1].startswith("1 ") and lines[2].startswith("2 "):
            return lines[0].strip(), lines[1], lines[2]

        # Case 2: 2-line format (no name)
        if len(lines) >= 2 and lines[0].startswith("1 ") and lines[1].startswith("2 "):
            return "", lines[0], lines[1]

        raise ValueError(f"Unexpected TLE format. Head:\n{tle_text[:200]}")

    @classmethod
    def from_lines(cls, line1: str, line2: str, name: str = "") -> "TLE":
        """
        Construct a TLE object from two TLE lines and optional object name.
        """
        # Normalize lines
        tle_line1 = line1.rstrip("\n")
        tle_line2 = line2.rstrip("\n")
        
        # =========================
        # -------- LINE 1 ---------
        # =========================

        sat_num = int(tle_line1[2:7])
        elset_class = tle_line1[7]
        int_designator = tle_line1[9:17].strip()

        epoch_year = int(tle_line1[18:20])
        epoch_day = float(tle_line1[20:32])

        year_full = 2000 + epoch_year if epoch_year < 57 else 1900 + epoch_year
        epoch_dt = datetime(year_full, 1, 1) + timedelta(days=epoch_day - 1)
        epoch_utc = epoch_dt.timestamp()

        n_dot = float(tle_line1[33:43])
        n_ddot = cls._parse_exponential(tle_line1[44:52])
        bstar = cls._parse_exponential(tle_line1[53:61])

        elem_set_type = int(tle_line1[62])
        elem_number = int(tle_line1[64:68])

        # =========================
        # -------- LINE 2 ---------
        # =========================

        inc = float(tle_line2[8:16])
        raan = float(tle_line2[17:25])
        ecc = float(f"0.{tle_line2[26:33].strip()}")
        argp = float(tle_line2[34:42])
        M = float(tle_line2[43:51])
        n = float(tle_line2[52:63])
        rev_num = int(tle_line2[63:68])

        return cls(
            name=name or "",
            sat_num=sat_num,
            elset_class=elset_class,
            int_designator=int_designator,
            epoch_utc=epoch_utc,
            epoch_year=epoch_year,
            epoch_day=epoch_day,
            n_dot=n_dot,
            n_ddot=n_ddot,
            bstar=bstar,
            elem_set_type=elem_set_type,
            elem_number=elem_number,
            inc=inc,
            raan=raan,
            ecc=ecc,
            argp=argp,
            M=M,
            n=n,
            rev_num=rev_num,
            line1=tle_line1,
            line2=tle_line2,
        )

    @classmethod
    def from_text(cls, tle_text: str) -> "TLE":
        """
        Construct a TLE object from raw TLE text.

        Supports:
            - 3-line format (name + line1 + line2)
            - 2-line format (line1 + line2)
        """
        object_name, tle_line1, tle_line2 = cls._extract_from_text(tle_text)

        return cls.from_lines(
            line1=tle_line1,
            line2=tle_line2,
            name=object_name,
        )