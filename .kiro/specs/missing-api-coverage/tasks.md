# Implementation Plan: Missing API Coverage

## Overview

This implementation plan expands the Washington State Legislature MCP Server with 25+ new tools covering roll call votes, amendments, committee actions, session laws, governor actions, enhanced sponsor/committee information, and document management. The implementation follows the existing architecture pattern and integrates seamlessly with the current WSLClient and FastMCP infrastructure.

## Tasks

- [x] 1. Set up WSLClient methods for new SOAP services
  - Add methods to WSLClient for all new WSLWS API operations
  - Implement connection pooling reuse for new services
  - Add error handling and retry logic for new operations
  - _Requirements: 17.2, 16.2, 16.3_

- [x] 2. Implement roll call and voting tools
  - [x] 2.1 Implement getRollCalls tool
    - Create MCP tool function with biennium and bill_number parameters
    - Call WSLClient.GetRollCalls SOAP operation
    - Parse response into roll call data structure with votes
    - Handle empty results and errors
    - _Requirements: 1.1, 1.2, 1.4, 1.5_
  
  - [x] 2.2 Write property test for roll call response structure
    - **Property 1: Response Structure Consistency**
    - **Validates: Requirements 1.2**
  
  - [x] 2.3 Write property test for chronological ordering
    - **Property 4: Chronological Ordering**
    - **Validates: Requirements 1.3**
  
  - [x] 2.4 Write unit tests for roll call edge cases
    - Test empty roll calls return descriptive message
    - Test invalid bill numbers return errors
    - _Requirements: 1.4, 1.5_

- [x] 3. Implement amendment tools
  - [x] 3.1 Implement getAmendmentsForBiennium tool
    - Create MCP tool with biennium and bill_number parameters
    - Call WSLClient.GetAmendmentsForBiennium
    - Parse amendment data with sponsor, status, description
    - _Requirements: 2.1, 2.3_
  
  - [x] 3.2 Implement getAmendmentsForYear tool
    - Create MCP tool with year and bill_number parameters
    - Support both 2-digit and 4-digit year formats
    - Call WSLClient.GetAmendmentsForYear
    - _Requirements: 2.2, 2.5_
  
  - [x] 3.3 Write property test for year format flexibility
    - **Property 8: Year Format Flexibility**
    - **Validates: Requirements 2.5**
  
  - [x] 3.4 Write property test for amendment retrieval
    - **Property 12: Amendment Retrieval by Biennium**
    - **Property 13: Amendment Retrieval by Year**
    - **Validates: Requirements 2.1, 2.2**

- [x] 4. Implement committee hearing and RCW citation tools
  - [x] 4.1 Implement getHearings tool
    - Create MCP tool with biennium and bill_number parameters
    - Call WSLClient.GetHearings
    - Parse hearing data with committee, date, time, location
    - Include revised meeting indicators
    - _Requirements: 3.1, 3.2, 3.5_
  
  - [x] 4.2 Implement getRcwCitesAffected tool
    - Create MCP tool with biennium and bill_number parameters
    - Call WSLClient.GetRcwCitesAffected
    - Parse RCW citations and group by action type
    - Format citations in standard RCW notation
    - _Requirements: 4.1, 4.2, 4.3, 4.5_
  
  - [x] 4.3 Write property test for RCW citation grouping
    - **Property 7: RCW Citation Grouping**
    - **Validates: Requirements 4.3**
  
  - [x] 4.4 Write property test for RCW notation formatting
    - **Property 10: RCW Notation Formatting**
    - **Validates: Requirements 4.5**

- [x] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 6. Implement session law tools
  - [ ] 6.1 Implement getSessionLawByBill tool
    - Create MCP tool with biennium and bill_number parameters
    - Call WSLClient.GetSessionLawByBill
    - Parse session law data with chapter, effective date, law text URL
    - Handle bills not enacted into law
    - _Requirements: 5.1, 5.5_
  
  - [ ] 6.2 Implement getSessionLawByBillId tool
    - Create MCP tool with bill_id parameter
    - Call WSLClient.GetSessionLawByBillId
    - _Requirements: 5.1_
  
  - [ ] 6.3 Implement getBillByChapterNumber tool
    - Create MCP tool with year and chapter_number parameters
    - Call WSLClient.GetBillByChapterNumber
    - Implement reverse lookup from chapter to bill
    - _Requirements: 5.2_
  
  - [ ] 6.4 Implement getChapterNumbersByYear tool
    - Create MCP tool with year parameter
    - Call WSLClient.GetChapterNumbersByYear
    - Return all session law chapters for the year
    - _Requirements: 5.3_
  
  - [ ] 6.5 Implement getSessionLawByInitiativeNumber tool
    - Create MCP tool with initiative_number and year parameters
    - Call WSLClient.GetSessionLawByInitiativeNumber
    - Handle initiative-specific data structure
    - _Requirements: 5.4_
  
  - [ ] 6.6 Write property tests for session law tools
    - **Property 16: Session Law Retrieval by Bill**
    - **Property 17: Session Law Reverse Lookup**
    - **Property 18: Annual Session Law Completeness**
    - **Property 19: Initiative Session Law Retrieval**
    - **Validates: Requirements 5.1, 5.2, 5.3, 5.4**

- [ ] 7. Implement governor action tools
  - [ ] 7.1 Implement getLegislationGovernorSigned tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetLegislationGovernorSigned
    - Parse signed bills with action dates
    - Support optional year filtering
    - _Requirements: 6.1, 6.4, 6.5_
  
  - [ ] 7.2 Implement getLegislationGovernorVeto tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetLegislationGovernorVeto
    - Include veto messages in response
    - _Requirements: 6.2, 6.4_
  
  - [ ] 7.3 Implement getLegislationGovernorPartialVeto tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetLegislationGovernorPartialVeto
    - Parse partial veto data with affected sections
    - _Requirements: 6.3, 6.4_
  
  - [ ] 7.4 Write property tests for governor action tools
    - **Property 20: Governor Signed Bills Retrieval**
    - **Property 21: Governor Vetoed Bills Retrieval**
    - **Property 22: Governor Partial Veto Retrieval**
    - **Validates: Requirements 6.1, 6.2, 6.3**
  
  - [ ] 7.5 Write property test for temporal filtering
    - **Property 6: Temporal Filtering Correctness**
    - **Validates: Requirements 6.5**

- [ ] 8. Implement committee action tools
  - [ ] 8.1 Implement getCommitteeExecutiveActionsByBill tool
    - Create MCP tool with biennium and bill_number parameters
    - Call WSLClient.GetCommitteeExecutiveActionsByBill
    - Parse executive actions with committee, date, action type
    - _Requirements: 7.1, 7.5_
  
  - [ ] 8.2 Implement getCommitteeReferralsByBill tool
    - Create MCP tool with biennium and bill_number parameters
    - Call WSLClient.GetCommitteeReferralsByBill
    - Parse referral history
    - _Requirements: 7.1, 7.5_
  
  - [ ] 8.3 Implement getCommitteeReferralsByCommittee tool
    - Create MCP tool with biennium and committee_name parameters
    - Call WSLClient.GetCommitteeReferralsByCommittee
    - Return bills referred to committee
    - _Requirements: 7.2_
  
  - [ ] 8.4 Implement getDoPassByCommittee tool
    - Create MCP tool with biennium and committee_name parameters
    - Call WSLClient.GetDoPassByCommittee
    - Filter bills with "do pass" recommendation
    - _Requirements: 7.3_
  
  - [ ] 8.5 Implement getInCommittee tool
    - Create MCP tool with biennium and committee_name parameters
    - Call WSLClient.GetInCommittee
    - Return currently referred bills
    - _Requirements: 7.2_
  
  - [ ] 8.6 Implement getLegislationReportedOutOfCommittee tool
    - Create MCP tool with biennium and committee_name parameters
    - Call WSLClient.GetLegislationReportedOutOfCommittee
    - Include recommendation type and vote counts
    - _Requirements: 7.4_
  
  - [ ] 8.7 Write property tests for committee action tools
    - **Property 23: Committee Action Retrieval**
    - **Property 24: Bills in Committee Retrieval**
    - **Property 25: Do Pass Filtering**
    - **Property 26: Reported Bills Include Recommendations**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 10. Implement enhanced committee information tools
  - [ ] 10.1 Implement getActiveCommittees tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetActiveCommittees
    - Return active committees for both chambers
    - _Requirements: 8.1, 8.5_
  
  - [ ] 10.2 Implement getActiveHouseCommittees tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetActiveHouseCommittees
    - Filter for House committees only
    - _Requirements: 8.1, 8.3, 8.5_
  
  - [ ] 10.3 Implement getActiveSenateCommittees tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetActiveSenateCommittees
    - Filter for Senate committees only
    - _Requirements: 8.1, 8.3, 8.5_
  
  - [ ] 10.4 Implement getActiveCommitteeMembers tool
    - Create MCP tool with biennium and committee_name parameters
    - Call WSLClient.GetActiveCommitteeMembers
    - Parse member data with roles, party, district, contact info
    - _Requirements: 8.2_
  
  - [ ] 10.5 Implement getCommitteeMembers tool
    - Create MCP tool with biennium and committee_name parameters
    - Call WSLClient.GetCommitteeMembers
    - Support historical committee composition
    - _Requirements: 8.2, 8.4_
  
  - [ ] 10.6 Implement getHouseCommittees tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetHouseCommittees
    - _Requirements: 8.1, 8.3_
  
  - [ ] 10.7 Implement getSenateCommittees tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetSenateCommittees
    - _Requirements: 8.1, 8.3_
  
  - [ ] 10.8 Write property tests for committee information tools
    - **Property 27: Active Committee Retrieval**
    - **Property 28: Historical Committee Composition**
    - **Validates: Requirements 8.1, 8.4**
  
  - [ ] 10.9 Write property test for chamber filtering
    - **Property 5: Chamber Filtering Correctness**
    - **Validates: Requirements 8.3**

- [ ] 11. Implement enhanced sponsor tools
  - [ ] 11.1 Implement getSponsors tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetSponsors
    - Parse sponsor data for both chambers
    - Include name, party, district, contact information
    - _Requirements: 9.1, 9.4_
  
  - [ ] 11.2 Implement getHouseSponsors tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetHouseSponsors
    - Filter for House sponsors
    - _Requirements: 9.1, 9.2, 9.4_
  
  - [ ] 11.3 Implement getSenateSponors tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetSenateSponsors
    - Filter for Senate sponsors
    - _Requirements: 9.1, 9.2, 9.4_
  
  - [ ] 11.4 Implement getRequesters tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetRequesters
    - Return entities authorized to request legislation
    - _Requirements: 9.3_
  
  - [ ] 11.5 Write property tests for sponsor tools
    - **Property 29: Sponsor Retrieval Completeness**
    - **Property 30: Requester Information Retrieval**
    - **Property 31: Sponsorship Count Aggregation**
    - **Validates: Requirements 9.1, 9.3, 9.5**

- [ ] 12. Implement bill passage and status tracking tools
  - [ ] 12.1 Implement getLegislationPassedHouse tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetLegislationPassedHouse
    - Parse passage data with dates and vote counts
    - Support optional year filtering
    - _Requirements: 11.1, 11.4, 11.5_
  
  - [ ] 12.2 Implement getLegislationPassedSenate tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetLegislationPassedSenate
    - Parse passage data with dates and vote counts
    - _Requirements: 11.2, 11.4, 11.5_
  
  - [ ] 12.3 Implement getLegislationPassedLegislature tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetLegislationPassedLegislature
    - Return only bills that passed both chambers
    - _Requirements: 11.3, 11.4_
  
  - [ ] 12.4 Implement getPrefiledLegislation tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetPrefiledLegislation
    - Parse prefiled bills with filing dates
    - Support chamber filtering
    - _Requirements: 12.1, 12.2, 12.3, 12.4_
  
  - [ ] 12.5 Implement getLegislativeStatusChanges tool
    - Create MCP tool with begin_date, end_date, and optional biennium parameters
    - Accept ISO 8601 date format
    - Call WSLClient.GetLegislativeStatusChanges
    - Parse status changes with old/new status and dates
    - _Requirements: 10.1, 10.2, 10.3, 10.5_
  
  - [ ] 12.6 Write property tests for passage tracking tools
    - **Property 33: House Passage Retrieval**
    - **Property 34: Senate Passage Retrieval**
    - **Property 35: Legislature Passage Retrieval**
    - **Property 36: Prefiled Legislation Retrieval**
    - **Validates: Requirements 11.1, 11.2, 11.3, 12.1**
  
  - [ ] 12.7 Write property test for status change tracking
    - **Property 32: Status Change Date Range Filtering**
    - **Validates: Requirements 10.1**
  
  - [ ] 12.8 Write property test for ISO 8601 date acceptance
    - **Property 9: ISO 8601 Date Acceptance**
    - **Validates: Requirements 10.5**

- [ ] 13. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 14. Implement document management tools
  - [ ] 14.1 Implement getDocumentClasses tool
    - Create MCP tool with biennium parameter
    - Call WSLClient.GetDocumentClasses
    - Parse document classes with names and descriptions
    - _Requirements: 13.1, 13.5_
  
  - [ ] 14.2 Implement getAllDocumentsByClass tool
    - Create MCP tool with biennium and document_class parameters
    - Call WSLClient.GetAllDocumentsByClass
    - Parse document list with names, URLs, bill associations
    - _Requirements: 13.2, 13.4_
  
  - [ ] 14.3 Implement getDocumentsByClass tool
    - Create MCP tool with biennium, document_class, and name_filter parameters
    - Call WSLClient.GetDocumentsByClass
    - Implement pattern matching for name filter
    - _Requirements: 13.3, 13.4_
  
  - [ ] 14.4 Write property tests for document management tools
    - **Property 37: Document Class Retrieval**
    - **Property 38: Document Class Filtering**
    - **Property 39: Document Name Pattern Matching**
    - **Validates: Requirements 13.1, 13.2, 13.3**

- [ ] 15. Implement metadata and reference tools
  - [ ] 15.1 Implement getLegislationTypes tool
    - Create MCP tool with no parameters
    - Call WSLClient.GetLegislationTypes
    - Parse legislation types with codes, descriptions, chamber applicability
    - Implement 24-hour caching with cache metadata
    - Handle API failure with default set and warning
    - _Requirements: 14.1, 14.2, 14.3, 14.5_
  
  - [ ] 15.2 Implement getLegislationByRequestNumber tool
    - Create MCP tool with biennium and request_number parameters
    - Call WSLClient.GetLegislationByRequestNumber
    - Parse bill information or pending request status
    - Handle invalid request numbers with descriptive errors
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
  
  - [ ] 15.3 Implement getCommitteeMeetingItems tool
    - Create MCP tool with meeting_id parameter
    - Call WSLClient.GetCommitteeMeetingItems
    - Parse agenda items with bills and topics
    - _Requirements: 3.2_
  
  - [ ] 15.4 Implement getRevisedCommitteeMeetings tool
    - Create MCP tool with since_date and optional biennium parameters
    - Accept ISO 8601 date format
    - Call WSLClient.GetRevisedCommitteeMeetings
    - _Requirements: 3.5, 10.5_
  
  - [ ] 15.5 Write property tests for metadata tools
    - **Property 40: Legislation Type Retrieval**
    - **Property 41: Legislation Type Caching**
    - **Property 42: Legislation Type Validation**
    - **Property 43: Request Number Lookup**
    - **Validates: Requirements 14.1, 14.3, 14.4, 15.1, 15.2**

- [ ] 16. Implement caching layer
  - [ ] 16.1 Create caching utility module
    - Implement cache decorator with TTL support
    - Use in-memory cache with configurable size limits
    - Add cache metadata to responses (cached flag, timestamp)
    - _Requirements: 18.1, 18.5_
  
  - [ ] 16.2 Apply caching to reference data tools
    - Cache getLegislationTypes for 24 hours
    - Cache getDocumentClasses for 24 hours
    - Add cache invalidation mechanism
    - _Requirements: 14.3, 18.1_
  
  - [ ] 16.3 Write property test for caching behavior
    - **Property 41: Legislation Type Caching**
    - **Validates: Requirements 14.3, 18.1, 18.5**

- [ ] 17. Implement pagination and performance features
  - [ ] 17.1 Create pagination utility
    - Implement pagination for responses with >100 items
    - Add configurable page size parameter
    - Include pagination metadata in responses
    - _Requirements: 18.3_
  
  - [ ] 17.2 Implement timeout handling
    - Add configurable timeout values per tool
    - Handle timeout errors with descriptive messages
    - Support environment variable configuration
    - _Requirements: 18.4_
  
  - [ ] 17.3 Write property tests for performance features
    - **Property 44: Pagination for Large Results**
    - **Property 45: Timeout Handling**
    - **Validates: Requirements 18.3, 18.4**

- [ ] 18. Implement comprehensive error handling
  - [ ] 18.1 Add input validation to all tools
    - Validate required parameters before API calls
    - Check parameter formats (dates, bill numbers, etc.)
    - Return descriptive validation errors
    - _Requirements: 16.4_
  
  - [ ] 18.2 Implement SOAP fault handling
    - Extract fault messages from SOAP responses
    - Convert to user-friendly error messages
    - Log full fault details
    - _Requirements: 16.2_
  
  - [ ] 18.3 Add retry logic for network errors
    - Implement exponential backoff (1s, 2s, 4s)
    - Retry up to 3 times on network failures
    - Log each retry attempt
    - _Requirements: 16.3_
  
  - [ ] 18.4 Write property tests for error handling
    - **Property 3: Error Handling Consistency**
    - **Validates: Requirements 1.5, 15.4, 16.2, 16.4**
  
  - [ ] 18.5 Write unit tests for error scenarios
    - Test invalid parameters return validation errors
    - Test SOAP faults are handled gracefully
    - Test network errors trigger retries
    - _Requirements: 16.2, 16.3, 16.4_

- [ ] 19. Implement comprehensive property tests
  - [ ] 19.1 Write property test for response structure consistency
    - **Property 1: Response Structure Consistency**
    - Test all tools return consistent Dict[str, Any] structure
    - **Validates: Requirements 1.2, 2.3, 3.2, 4.2, 6.4, 7.5, 8.2, 8.5, 9.4, 10.2, 11.4, 12.2, 13.4, 13.5, 14.2, 15.2**
  
  - [ ] 19.2 Write property test for empty result handling
    - **Property 2: Empty Result Handling**
    - Test all tools handle empty results with descriptive messages
    - **Validates: Requirements 1.4, 2.4, 3.4, 4.4, 5.5, 10.4, 12.5**
  
  - [ ] 19.3 Write property test for return type consistency
    - **Property 46: Return Type Consistency**
    - Test all tools return Dict[str, Any]
    - **Validates: Requirements 17.3**
  
  - [ ] 19.4 Write property test for optional parameter defaults
    - **Property 47: Optional Parameter Defaults**
    - Test all tools with optional parameters use sensible defaults
    - **Validates: Requirements 17.4**

- [ ] 20. Integration and documentation
  - [ ] 20.1 Register all new tools with FastMCP
    - Add tool decorators and metadata
    - Include parameter descriptions and examples
    - Ensure consistent naming conventions
    - _Requirements: 17.1, 17.5_
  
  - [ ] 20.2 Update WSLClient with all new SOAP methods
    - Verify connection pooling works with new services
    - Test SOAP client reuse across tools
    - _Requirements: 17.2_
  
  - [ ] 20.3 Add comprehensive logging
    - Log all API calls with parameters
    - Log errors with full context
    - Log successful responses with summaries
    - _Requirements: 16.1, 16.5_
  
  - [ ] 20.4 Write integration tests
    - Test end-to-end flows across multiple tools
    - Test WSLClient connection pooling
    - Test caching behavior across tool calls
    - Test retry logic with simulated failures
    - _Requirements: 17.2, 18.1_

- [ ] 21. Final checkpoint - Ensure all tests pass
  - Run full test suite (unit, property, integration)
  - Verify test coverage meets 85%+ goal
  - Ensure all 47 correctness properties are tested
  - Ask the user if questions arise.

## Notes

- All tasks are required for comprehensive implementation with full test coverage
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at reasonable breaks
- Property tests validate universal correctness properties (100+ iterations each)
- Unit tests validate specific examples and edge cases
- Integration tests validate component interactions and end-to-end flows
- All new tools follow existing patterns for consistency
- Caching improves performance for reference data
- Comprehensive error handling ensures robustness
