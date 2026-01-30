"""
Washington State Legislature API Client

A thin wrapper around the wa-leg-api library for consistent error handling
and potential future enhancements.
"""

import logging
from typing import Any, Dict, List, Optional

from wa_leg_api.amendment import get_amendments
from wa_leg_api.committee import (
    get_active_committee_members,
    get_active_committees,
    get_active_house_committees,
    get_active_senate_committees,
    get_committee_members,
    get_committees,
    get_house_committees,
    get_senate_committees,
)
from wa_leg_api.committeeaction import (
    get_committee_executive_actions_by_bill,
    get_committee_referrals_by_bill,
    get_committee_referrals_by_committee,
    get_do_pass_by_committee,
    get_in_committee,
    get_legislation_reported_out_of_committee,
)
from wa_leg_api.committeemeeting import (
    get_committee_meeting_items,
    get_committee_meetings,
    get_revised_committee_meetings,
)
from wa_leg_api.legislation import (
    get_amendments_for_biennium,
    get_amendments_for_year,
    get_hearings,
    get_legislation,
    get_legislation_by_request_number,
    get_legislation_by_year,
    get_legislation_governor_partial_veto,
    get_legislation_governor_signed,
    get_legislation_governor_veto,
    get_legislation_passed_house,
    get_legislation_passed_legislature,
    get_legislation_passed_senate,
    get_legislation_types,
    get_legislative_status_changes_by_date_range,
    get_prefiled_legislation,
    get_rcw_cites_affected,
    get_roll_calls,
)
from wa_leg_api.legislativedocument import (
    get_all_documents_by_class,
    get_document_classes,
    get_documents,
    get_documents_by_class,
)
from wa_leg_api.sessionlaw import (
    get_bill_by_chapter_number,
    get_chapter_numbers_by_year,
    get_session_law_by_bill,
    get_session_law_by_bill_id,
    get_session_law_by_initiative_number,
)
from wa_leg_api.sponsor import (
    get_house_sponsors,
    get_requesters,
    get_senate_sponsors,
    get_sponsors,
)

logger = logging.getLogger(__name__)


class WSLClient:
    """
    Client for interacting with Washington State Legislature APIs.

    This is a thin wrapper around the wa-leg-api library that provides consistent error handling and logging.
    """

    def get_legislation(self, biennium: str, bill_number: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get information about a specific bill.

        Example Response: [
            {
                'biennium': '2025-26',
                'bill_id': 'HB 1000',
                'bill_number': '1000',
                'substitute_version': '0',
                'engrossed_version': '0',
                'short_legislation_type': {
                    'short_legislation_type': 'B',
                    'long_legislation_type': 'Bill'
                },
                'original_agency': 'House',
                'active': True,
                'state_fiscal_note': False,
                'local_fiscal_note': False,
                'appropriations': False,
                'requested_by_governor': False,
                'requested_by_budget_committee': False,
                'requested_by_department': False,
                'requested_by_other': False,
                'short_description': 'Controlled subst. violations',
                'request': 'H-0097.1',
                'introduced_date': datetime.datetime(2025, 1, 13, 0, 0),
                'current_status': {
                    'bill_id': 'HB 1000',
                    'history_line': 'First reading, referred to Community Safety.',
                    'action_date': datetime.datetime(2025, 1, 13, 0, 0),
                    'amended_by_opposite_body': False,
                    'partial_veto': False,
                    'veto': False,
                    'amendments_exist': False,
                    'status': 'H Community Safe'
                },
                'sponsor': '(Walsh)',
                'prime_sponsor_i_d': 27181,
                'long_description': 'Expanding the circumstances that may constitute a major violation of the uniform controlled substances act.',
                'legal_title': 'AN ACT Relating to expanding the circumstances that may constitute a major violation of the uniform controlled substances act;',
                'companions': None
            }
        ]
        """
        try:
            result = get_legislation(biennium, bill_number)
            return result.get("array_of_legislation", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get legislation {bill_number} for {biennium}: {e}")
            return None

    def get_legislation_by_year(self, year: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get all legislation for a specific year.

        Example Response: [
            {
                'biennium': '2025-26',
                'bill_id': 'HB 1000',
                'bill_number': 1000,
                'substitute_version': 0,
                'engrossed_version': 0,
                'short_legislation_type': {
                    'short_legislation_type': 'B',
                    'long_legislation_type': 'Bill'
                },
                'original_agency': 'House',
                'active': True
            }
        ]
        """
        try:
            result = get_legislation_by_year(year)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get legislation for year {year}: {e}")
            return None

    def get_committees(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get list of committees for a biennium.

        Example Response: [
            {
                'id': '31649',
                'name': 'Agriculture & Natural Resources',
                'long_name': 'House Committee on Agriculture & Natural Resources',
                'agency': 'House',
                'acronym': 'AGNR',
                'phone': '(360) 786-7339'
            }
        ]
        """
        try:
            result = get_committees(biennium)
            return result.get("array_of_committee", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get committees for {biennium}: {e}")
            return None

    def get_committee_meetings(
        self, begin_date: str, end_date: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get committee meetings for a date range.

        Example Response: [
            {
                'agenda_id': 32300,
                'agency': 'Joint',
                'committees': [
                    {
                        'id': '27992',
                        'name': 'Joint Committee on Employment Relations',
                        'long_name': 'Joint Joint Committee on Employment Relations',
                        'agency': 'Joint',
                        'acronym': 'JCER',
                        'phone': None
                    }
                ],
                'room': 'Virtual',
                'building': None,
                'address': ',',
                'city': None,
                'state': '',
                'zip_code': 0,
                'date': datetime.datetime(2025, 1, 9, 14, 0),
                'cancelled': False,
                'revised_date': datetime.datetime(1, 1, 1, 0, 0),
                'contact_information': None,
                'committee_type': 'Full Committee',
                'notes': "To view committee meetings or access the committee meeting documents, visit the Legislature's committee schedules, agendas, and documents website: https://app.leg.wa.gov/committeeschedules"
            }
        ]
        """
        try:
            result = get_committee_meetings(begin_date, end_date)
            return result.get("array_of_committee_meeting", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get committee meetings from {begin_date} to {end_date}: {e}")
            return None

    def get_sponsors(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get list of sponsors/legislators for a biennium.

        Example Response: [
            {
                'id': '31526',
                'name': 'Peter Abbarno',
                'long_name': 'Representative Abbarno',
                'agency': 'House',
                'acronym': 'ABBA',
                'party': 'R',
                'district': '20',
                'phone': '(360) 786-7896',
                'email': 'Peter.Abbarno@leg.wa.gov',
                'first_name': 'Peter',
                'last_name': 'Abbarno'
            }
        ]
        """
        try:
            result = get_sponsors(biennium)
            return result.get("array_of_member", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get sponsors for {biennium}: {e}")
            return None

    def get_amendments(self, year: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get amendments for a specific bill.

        Example Response: [
            {
                'bill_number': 5195,
                'name': '5195-S AMH THAR H2391.1',
                'bill_id': 'SSB 5195',
                'legislative_session': '2025 Regular Session',
                'type': 'Floor',
                'floor_number': 1457,
                'sponsor_name': 'Tharinger',
                'description': 'Striker',
                'drafter': 'H2391.1',
                'floor_action': 'ADOPTED',
                'floor_action_date': datetime.datetime(2025, 4, 27, 0, 0),
                'document_exists': True,
                'htm_url': 'http://lawfilesext.leg.wa.gov/biennium/2025-26/Htm/Amendments/House/5195-S AMH THAR H2391.1.htm',
                'pdf_url': 'http://lawfilesext.leg.wa.gov/biennium/2025-26/Pdf/Amendments/House/5195-S AMH THAR H2391.1.pdf',
                'agency': 'House'
            }
        ]
        """
        try:
            result = get_amendments(year)
            return result.get("array_of_amendment", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get amendments in {year}: {e}")
            return None

    def get_documents(self, biennium: str, bill_number: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get documents for a specific bill.

        Example Response: [
            {
                'name': '1000',
                'short_friendly_name': 'Original Bill',
                'biennium': '2025-26',
                'long_friendly_name': 'House Bill 1000',
                'description': None,
                'type': 'House Bills',
                'class': 'Bills',
                'htm_url': 'http://lawfilesext.leg.wa.gov/biennium/2025-26/Htm/Bills/House Bills/1000.htm',
                'htm_create_date': datetime.datetime(2024, 12, 2, 14, 22, 43, 770000),
                'htm_last_modified_date': datetime.datetime(2024, 12, 2, 14, 22, 43, 770000),
                'pdf_url': 'http://lawfilesext.leg.wa.gov/biennium/2025-26/Pdf/Bills/House Bills/1000.pdf',
                'pdf_create_date': datetime.datetime(2024, 12, 2, 14, 22, 43, 970000),
                'pdf_last_modified_date': datetime.datetime(2024, 12, 2, 14, 22, 43, 970000),
                'bill_id': 'HB 1000'
            }
        ]
        """
        try:
            result = get_documents(biennium, bill_number)
            return result.get("array_of_legislative_document", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get documents for {bill_number} in {biennium}: {e}")
            return None

    # Roll Call and Voting Methods

    def get_roll_calls(self, biennium: str, bill_number: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get roll call votes for a bill.

        Args:
            biennium: Biennium in format "2023-24"
            bill_number: Bill number (e.g., 1234 for HB 1234)

        Returns:
            List of roll call votes with legislator names, votes, and dates
        """
        try:
            result = get_roll_calls(biennium, bill_number)
            return result.get("array_of_roll_call", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get roll calls for bill {bill_number} in {biennium}: {e}")
            return None

    # Amendment Methods

    def get_amendments_for_biennium(
        self, biennium: str, bill_number: int
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get amendments for a bill in a biennium.

        Args:
            biennium: Biennium in format "2023-24"
            bill_number: Bill number (e.g., 1234 for HB 1234)

        Returns:
            List of amendments with sponsor, description, and status
        """
        try:
            result = get_amendments_for_biennium(biennium, bill_number)
            return result.get("array_of_amendment", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get amendments for bill {bill_number} in biennium {biennium}: {e}"
            )
            return None

    def get_amendments_for_year(self, year: int, bill_number: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get amendments for a bill in a specific year.

        Args:
            year: Year (e.g., 2023 or 23)
            bill_number: Bill number (e.g., 1234 for HB 1234)

        Returns:
            List of amendments
        """
        try:
            result = get_amendments_for_year(year, bill_number)
            return result.get("array_of_amendment", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get amendments for bill {bill_number} in year {year}: {e}")
            return None

    # Committee Hearing and RCW Citation Methods

    def get_hearings(self, biennium: str, bill_number: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get committee hearings for a bill.

        Args:
            biennium: Biennium in format "2023-24"
            bill_number: Bill number (e.g., 1234 for HB 1234)

        Returns:
            List of hearings with committee, date, time, location, and agenda
        """
        try:
            result = get_hearings(biennium, bill_number)
            return result.get("array_of_committee_meeting", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get hearings for bill {bill_number} in {biennium}: {e}")
            return None

    def get_rcw_cites_affected(self, biennium: str, bill_id: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get RCW sections affected by a bill.

        Args:
            biennium: Biennium in format "2023-24"
            bill_id: Bill ID (e.g., "HB 1234")

        Returns:
            List of RCW citations with section numbers and action types
        """
        try:
            result = get_rcw_cites_affected(biennium, bill_id)
            return result.get("array_of_rcw_cite", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get RCW cites for {bill_id} in {biennium}: {e}")
            return None

    # Session Law Methods

    def get_session_law_by_bill(
        self, biennium: str, bill_number: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get session law information for a bill.

        Args:
            biennium: Biennium in format "2023-24"
            bill_number: Bill number (e.g., 1234 for HB 1234)

        Returns:
            Session law with chapter number, effective date, and law text reference
        """
        try:
            result = get_session_law_by_bill(biennium, bill_number)
            return result.get("session_law", None) if result else None
        except Exception as e:
            logger.error(f"Failed to get session law for bill {bill_number} in {biennium}: {e}")
            return None

    def get_session_law_by_bill_id(self, biennium: str, bill_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session law by bill ID.

        Args:
            biennium: Biennium in format "2023-24"
            bill_id: Bill ID (e.g., "HB 1234")

        Returns:
            Session law information
        """
        try:
            result = get_session_law_by_bill_id(biennium, bill_id)
            return result.get("session_law", None) if result else None
        except Exception as e:
            logger.error(f"Failed to get session law for {bill_id} in {biennium}: {e}")
            return None

    def get_bill_by_chapter_number(
        self, year: int, session: int, chapter_number: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get bill information by session law chapter number.

        Args:
            year: Year (e.g., 2023)
            session: Session code (0=Regular, 1=1st Special, etc.)
            chapter_number: Chapter number

        Returns:
            Bill information
        """
        try:
            result = get_bill_by_chapter_number(year, session, chapter_number)
            return result.get("legislation", None) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get bill for chapter {chapter_number} in year {year} session {session}: {e}"
            )
            return None

    def get_chapter_numbers_by_year(self, year: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get all session law chapters for a year.

        Args:
            year: Year (e.g., 2023)

        Returns:
            List of session law chapters
        """
        try:
            result = get_chapter_numbers_by_year(year)
            return result.get("array_of_session_law", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get chapter numbers for year {year}: {e}")
            return None

    def get_session_law_by_initiative_number(
        self, initiative_number: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get session law for an initiative.

        Args:
            initiative_number: Initiative number (e.g., 1234 for I-1234)

        Returns:
            Initiative session law information
        """
        try:
            result = get_session_law_by_initiative_number(initiative_number)
            return result.get("session_law", None) if result else None
        except Exception as e:
            logger.error(f"Failed to get session law for initiative {initiative_number}: {e}")
            return None

    # Governor Action Methods

    def get_legislation_governor_signed(
        self, biennium: str, agency: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills signed by the governor.

        Args:
            biennium: Biennium in format "2023-24"
            agency: "House" or "Senate"

        Returns:
            List of signed bills with dates
        """
        try:
            result = get_legislation_governor_signed(biennium, agency)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get governor signed bills for {agency} in {biennium}: {e}")
            return None

    def get_legislation_governor_veto(
        self, biennium: str, agency: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills vetoed by the governor.

        Args:
            biennium: Biennium in format "2023-24"
            agency: "House" or "Senate"

        Returns:
            List of vetoed bills with veto messages
        """
        try:
            result = get_legislation_governor_veto(biennium, agency)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get governor vetoed bills for {agency} in {biennium}: {e}")
            return None

    def get_legislation_governor_partial_veto(
        self, biennium: str, agency: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills partially vetoed by the governor.

        Args:
            biennium: Biennium in format "2023-24"
            agency: "House" or "Senate"

        Returns:
            List of partially vetoed bills with affected sections
        """
        try:
            result = get_legislation_governor_partial_veto(biennium, agency)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get governor partially vetoed bills for {agency} in {biennium}: {e}"
            )
            return None

    # Committee Action Methods

    def get_committee_executive_actions_by_bill(
        self, biennium: str, bill_number: int
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get executive actions taken on a bill by committees.

        Args:
            biennium: Biennium in format "2023-24"
            bill_number: Bill number (e.g., 1234 for HB 1234)

        Returns:
            List of executive actions with committee, date, and action type
        """
        try:
            result = get_committee_executive_actions_by_bill(biennium, bill_number)
            return result.get("array_of_committee_executive_action", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get committee executive actions for bill {bill_number} in {biennium}: {e}"
            )
            return None

    def get_committee_referrals_by_bill(
        self, biennium: str, bill_number: int
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get committee referrals for a bill.

        Args:
            biennium: Biennium in format "2023-24"
            bill_number: Bill number (e.g., 1234 for HB 1234)

        Returns:
            List of referrals with committees and dates
        """
        try:
            result = get_committee_referrals_by_bill(biennium, bill_number)
            return result.get("array_of_committee_referral", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get committee referrals for bill {bill_number} in {biennium}: {e}"
            )
            return None

    def get_committee_referrals_by_committee(
        self, biennium: str, agency: str, committee_name: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills referred to a specific committee.

        Args:
            biennium: Biennium in format "2023-24"
            agency: "House" or "Senate"
            committee_name: Committee name

        Returns:
            List of referred bills
        """
        try:
            result = get_committee_referrals_by_committee(biennium, agency, committee_name)
            return result.get("array_of_committee_referral", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get committee referrals for {committee_name} in {biennium}: {e}"
            )
            return None

    def get_do_pass_by_committee(
        self, biennium: str, agency: str, committee_name: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills with "do pass" recommendation from a committee.

        Args:
            biennium: Biennium in format "2023-24"
            agency: "House" or "Senate"
            committee_name: Committee name

        Returns:
            List of bills with do pass recommendation
        """
        try:
            result = get_do_pass_by_committee(biennium, agency, committee_name)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get do pass bills for {committee_name} in {biennium}: {e}"
            )
            return None

    def get_in_committee(
        self, biennium: str, agency: str, committee_name: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills currently in a committee.

        Args:
            biennium: Biennium in format "2023-24"
            agency: "House" or "Senate"
            committee_name: Committee name

        Returns:
            List of bills currently referred to committee
        """
        try:
            result = get_in_committee(biennium, agency, committee_name)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get bills in committee {committee_name} in {biennium}: {e}"
            )
            return None

    def get_legislation_reported_out_of_committee(
        self, committee_name: str, agency: str, begin_date: str, end_date: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills reported out of a committee.

        Args:
            committee_name: Committee name
            agency: "House" or "Senate"
            begin_date: Begin date in ISO 8601 format
            end_date: End date in ISO 8601 format

        Returns:
            List of bills reported out with recommendation and votes
        """
        try:
            from datetime import datetime

            begin_dt = datetime.fromisoformat(begin_date)
            end_dt = datetime.fromisoformat(end_date)
            result = get_legislation_reported_out_of_committee(
                committee_name, agency, begin_dt, end_dt
            )
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get bills reported out of {committee_name} from {begin_date} to {end_date}: {e}"
            )
            return None

    # Enhanced Committee Information Methods

    def get_active_committees(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all currently active committees.

        Returns:
            List of active committees for both chambers
        """
        try:
            result = get_active_committees()
            return result.get("array_of_committee", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get active committees: {e}")
            return None

    def get_active_house_committees(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get active House committees.

        Returns:
            List of active House committees
        """
        try:
            result = get_active_house_committees()
            return result.get("array_of_committee", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get active House committees: {e}")
            return None

    def get_active_senate_committees(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get active Senate committees.

        Returns:
            List of active Senate committees
        """
        try:
            result = get_active_senate_committees()
            return result.get("array_of_committee", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get active Senate committees: {e}")
            return None

    def get_active_committee_members(
        self, agency: str, committee_name: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get members of an active committee.

        Args:
            agency: "House" or "Senate"
            committee_name: Committee name

        Returns:
            List of members with names, roles, party, district
        """
        try:
            result = get_active_committee_members(agency, committee_name)
            return result.get("array_of_member", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get active members for {committee_name}: {e}")
            return None

    def get_committee_members(
        self, biennium: str, agency: str, committee_name: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get committee members for a biennium (historical).

        Args:
            biennium: Biennium in format "2023-24"
            agency: "House" or "Senate"
            committee_name: Committee name

        Returns:
            List of committee members
        """
        try:
            result = get_committee_members(biennium, agency, committee_name)
            return result.get("array_of_member", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get committee members for {committee_name} in {biennium}: {e}"
            )
            return None

    def get_house_committees(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get all House committees for a biennium.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of House committees
        """
        try:
            result = get_house_committees(biennium)
            return result.get("array_of_committee", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get House committees for {biennium}: {e}")
            return None

    def get_senate_committees(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get all Senate committees for a biennium.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of Senate committees
        """
        try:
            result = get_senate_committees(biennium)
            return result.get("array_of_committee", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get Senate committees for {biennium}: {e}")
            return None

    # Enhanced Sponsor Methods

    def get_house_sponsors(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get House sponsors.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of House sponsor information
        """
        try:
            result = get_house_sponsors(biennium)
            return result.get("array_of_member", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get House sponsors for {biennium}: {e}")
            return None

    def get_senate_sponsors(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get Senate sponsors.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of Senate sponsor information
        """
        try:
            result = get_senate_sponsors(biennium)
            return result.get("array_of_member", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get Senate sponsors for {biennium}: {e}")
            return None

    def get_requesters(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get entities authorized to request legislation.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of requester information
        """
        try:
            result = get_requesters(biennium)
            return result.get("array_of_requester", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get requesters for {biennium}: {e}")
            return None

    # Bill Passage and Status Tracking Methods

    def get_legislation_passed_house(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills that passed the House.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of House-passed bills with passage dates and votes
        """
        try:
            result = get_legislation_passed_house(biennium)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get House-passed bills for {biennium}: {e}")
            return None

    def get_legislation_passed_senate(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills that passed the Senate.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of Senate-passed bills with passage dates and votes
        """
        try:
            result = get_legislation_passed_senate(biennium)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get Senate-passed bills for {biennium}: {e}")
            return None

    def get_legislation_passed_legislature(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get bills that passed both chambers.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of bills that passed both House and Senate
        """
        try:
            result = get_legislation_passed_legislature(biennium)
            return result.get("array_of_legislation_info", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get legislature-passed bills for {biennium}: {e}")
            return None

    def get_prefiled_legislation(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get prefiled bills.

        Returns:
            List of prefiled bills with filing dates
        """
        try:
            result = get_prefiled_legislation()
            return result.get("array_of_legislation", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get prefiled legislation: {e}")
            return None

    def get_legislative_status_changes(
        self, biennium: str, begin_date: str, end_date: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get bill status changes in a date range.

        Args:
            biennium: Biennium in format "2023-24"
            begin_date: Begin date in ISO 8601 format
            end_date: End date in ISO 8601 format

        Returns:
            List of status changes with old/new status and dates
        """
        try:
            from datetime import datetime

            begin_dt = datetime.fromisoformat(begin_date)
            end_dt = datetime.fromisoformat(end_date)
            result = get_legislative_status_changes_by_date_range(biennium, begin_dt, end_dt)
            return result.get("array_of_legislative_status_change", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get status changes for {biennium} from {begin_date} to {end_date}: {e}"
            )
            return None

    # Document Management Methods

    def get_document_classes(self, biennium: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get available document types for a biennium.

        Args:
            biennium: Biennium in format "2023-24"

        Returns:
            List of document classes with names and descriptions
        """
        try:
            result = get_document_classes(biennium)
            return result.get("array_of_document_class", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get document classes for {biennium}: {e}")
            return None

    def get_all_documents_by_class(
        self, biennium: str, document_class: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get all documents of a specific class.

        Args:
            biennium: Biennium in format "2023-24"
            document_class: Document class (e.g., "Bills", "Amendments")

        Returns:
            List of documents with names, URLs, bill associations
        """
        try:
            result = get_all_documents_by_class(biennium, document_class)
            return result.get("array_of_legislative_document", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get documents for class {document_class} in {biennium}: {e}"
            )
            return None

    def get_documents_by_class(
        self, biennium: str, document_class: str, name_filter: str
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get documents by class with name filter.

        Args:
            biennium: Biennium in format "2023-24"
            document_class: Document class (e.g., "Bills")
            name_filter: Pattern to match (e.g., "HB 1*")

        Returns:
            List of filtered documents
        """
        try:
            result = get_documents_by_class(biennium, document_class, name_filter)
            return result.get("array_of_legislative_document", []) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get documents for class {document_class} with filter {name_filter} in {biennium}: {e}"
            )
            return None

    # Metadata and Reference Methods

    def get_legislation_types(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get valid legislation types.

        Returns:
            List of legislation type codes and descriptions
        """
        try:
            result = get_legislation_types()
            return result.get("array_of_legislation_type", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get legislation types: {e}")
            return None

    def get_legislation_by_request_number(
        self, biennium: str, request_number: str
    ) -> Optional[Dict[str, Any]]:
        """
        Look up bill by original request number.

        Args:
            biennium: Biennium in format "2023-24"
            request_number: Request number (e.g., "23-1234")

        Returns:
            Bill information or request status
        """
        try:
            result = get_legislation_by_request_number(biennium, request_number)
            return result.get("legislation", None) if result else None
        except Exception as e:
            logger.error(
                f"Failed to get legislation by request number {request_number} in {biennium}: {e}"
            )
            return None

    def get_committee_meeting_items(self, agenda_id: int) -> Optional[List[Dict[str, Any]]]:
        """
        Get agenda items for a specific committee meeting.

        Args:
            agenda_id: Meeting identifier

        Returns:
            List of agenda items with bills and topics
        """
        try:
            result = get_committee_meeting_items(agenda_id)
            return result.get("array_of_committee_meeting_item", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get meeting items for agenda {agenda_id}: {e}")
            return None

    def get_revised_committee_meetings(self, since_date: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get committee meetings revised since a date.

        Args:
            since_date: Date in ISO 8601 format

        Returns:
            List of revised meetings
        """
        try:
            from datetime import datetime

            since_dt = datetime.fromisoformat(since_date)
            result = get_revised_committee_meetings(since_dt)
            return result.get("array_of_committee_meeting", []) if result else None
        except Exception as e:
            logger.error(f"Failed to get revised meetings since {since_date}: {e}")
            return None
