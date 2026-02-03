# Washington State Legislature MCP Server

A Model Context Protocol (MCP) server that provides AI assistants with access to Washington State Legislature data, enabling civic engagement through conversational interfaces.

## Overview

This MCP server connects AI assistants to the Washington State Legislative Web Services (WSLWS), providing comprehensive tools for:
- Bill tracking and information retrieval
- Roll call votes and legislator voting records
- Amendments and bill modifications
- Committee meetings, actions, and membership
- Session laws and RCW citations
- Governor actions (signed, vetoed, partially vetoed bills)
- Sponsor and legislator information
- Bill passage tracking and status changes
- Legislative document management
- Metadata and reference data

With 35 MCP tools covering the full WSLWS API, this server enables AI assistants to answer complex questions about the Washington State legislative process and support civic engagement use cases.

## Features

This server provides **35 MCP tools** organized into logical categories:

### Bill Information Tools (8 tools)
- `getBillInfo` - Retrieve detailed information about specific bills
- `searchBills` - Search for bills using keywords and optional filtering
- `getBillsByYear` - Retrieve all bills from a specific year with filtering options
- `getBillStatus` - Get current status and history of a bill
- `getBillDocuments` - Retrieve bill document metadata with links
- `getBillContent` - Retrieve the actual content of a bill in AI-friendly format
- `getBillAmendments` - Get amendments for a specific bill
- `getCommittees` - Get committee information

### Roll Call and Voting Tools (1 tool)
- `getRollCalls` - Get roll call voting records for a bill with legislator votes

### Amendment Tools (2 tools)
- `getAmendmentsForBiennium` - Get amendments for a bill in a biennium
- `getAmendmentsForYear` - Get amendments for a bill in a specific year

### Committee Tools (9 tools)
- `getCommitteeMeetings` - Get committee meeting schedules and agendas
- `getActiveCommittees` - Get all currently active committees
- `getActiveHouseCommittees` - Get active House committees
- `getActiveSenateCommittees` - Get active Senate committees
- `getActiveCommitteeMembers` - Get members of an active committee
- `getCommitteeMembers` - Get committee members for a biennium (historical)
- `getHouseCommittees` - Get all House committees for a biennium
- `getSenateCommittees` - Get all Senate committees for a biennium
- `getCommitteeMeetingItems` - Get agenda items for a specific meeting

### Committee Action Tools (6 tools)
- `getCommitteeExecutiveActionsByBill` - Get executive actions on a bill
- `getCommitteeReferralsByBill` - Get committee referrals for a bill
- `getCommitteeReferralsByCommittee` - Get bills referred to a committee
- `getDoPassByCommittee` - Get bills with "do pass" recommendation
- `getInCommittee` - Get bills currently in a committee
- `getLegislationReportedOutOfCommittee` - Get bills reported out with recommendations

### Session Law and RCW Tools (7 tools)
- `getSessionLawByBill` - Get session law information for a bill
- `getSessionLawByBillId` - Get session law by bill ID
- `getBillByChapterNumber` - Get bill by session law chapter number
- `getChapterNumbersByYear` - Get all session law chapters for a year
- `getSessionLawByInitiativeNumber` - Get session law for an initiative
- `getRcwCitesAffected` - Get RCW sections affected by a bill
- `getHearings` - Get committee hearings for a bill

### Governor Action Tools (3 tools)
- `getLegislationGovernorSigned` - Get bills signed by the governor
- `getLegislationGovernorVeto` - Get bills vetoed by the governor
- `getLegislationGovernorPartialVeto` - Get bills with line-item vetoes

### Sponsor and Legislator Tools (5 tools)
- `findLegislator` - Find legislators by district or lookup sponsors
- `getSponsors` - Get all sponsors for a biennium
- `getHouseSponsors` - Get House sponsors
- `getSenateSponors` - Get Senate sponsors
- `getRequesters` - Get entities authorized to request legislation

### Bill Passage and Status Tools (5 tools)
- `getLegislationPassedHouse` - Get bills that passed the House
- `getLegislationPassedSenate` - Get bills that passed the Senate
- `getLegislationPassedLegislature` - Get bills that passed both chambers
- `getPrefiledLegislation` - Get prefiled bills
- `getLegislativeStatusChanges` - Get bill status changes in a date range

### Document Management Tools (3 tools)
- `getDocumentClasses` - Get available document types for a biennium
- `getAllDocumentsByClass` - Get all documents of a specific class
- `getDocumentsByClass` - Get documents by class with name filter

### Metadata and Reference Tools (4 tools)
- `getLegislationTypes` - Get valid legislation types (cached for 24 hours)
- `getLegislationByRequestNumber` - Look up bill by request number
- `getRevisedCommitteeMeetings` - Get committee meetings revised since a date
- `getCommitteeMeetingItems` - Get agenda items for a specific meeting

### MCP Resources
- `bill://xml/{biennium}/{chamber}/{bill_number}` - Access bill documents in structured XML format
- `bill://htm/{biennium}/{chamber}/{bill_number}` - Access bill documents in HTML format
- `bill://pdf/{biennium}/{chamber}/{bill_number}` - Get URLs for bill PDF documents
- `bill://document/{format}/{biennium}/{chamber}/{bill_number}` - Generic format for accessing bill documents


## Installation

### Prerequisites
- Python 3.10+
- pip package manager

### Development Installation
```bash
pip install -e ".[dev]"
```

### Production Installation
```bash
pip install .
```

## Quick Start

### Local Development
```bash
# Test with MCP Inspector
mcp dev src/wa_leg_mcp/server.py

# Run with stdio transport
python src/wa_leg_mcp/server.py
```

### Remote Deployment
For cloud deployment on AWS Lambda, you can use the `mcp-remote` adapter to enable Claude Desktop connectivity:
```json
{
  "mcpServers": {
    "wa-leg": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://your-api-gateway-url/sse"
      ]
    }
  }
}
```

### Basic Configuration
Create a `.env` file:
```env
WSL_API_TIMEOUT=30
WSL_CACHE_TTL=300
LOG_LEVEL=INFO
SERVER_NAME="Washington State Legislature MCP Server"
```

## Repository Structure

```
wa-leg-mcp/
├── src/wa_leg_mcp/
│   ├── server.py                    # Main MCP server
│   ├── clients/                     # API clients
│   │   ├── wsl_client.py           # SOAP API wrapper
│   │   └── wsl_search_client.py    # Search API client
│   ├── tools/                       # 35 MCP tools organized by function
│   │   ├── bill_tools.py           # Bill information and search
│   │   ├── roll_call_tools.py      # Voting records
│   │   ├── amendment_tools.py      # Bill amendments
│   │   ├── committee_tools.py      # Committee meetings
│   │   ├── enhanced_committee_tools.py  # Committee membership
│   │   ├── committee_action_tools.py    # Committee actions
│   │   ├── session_law_tools.py    # Session laws (not implemented yet)
│   │   ├── rcw_tools.py            # RCW citations and hearings
│   │   ├── governor_action_tools.py     # Governor actions (not implemented yet)
│   │   ├── sponsor_tools.py        # Sponsor information
│   │   ├── passage_tools.py        # Bill passage tracking
│   │   ├── document_tools.py       # Document management
│   │   ├── metadata_tools.py       # Reference data
│   │   └── legislator_tools.py     # Legislator lookup
│   ├── resources/                   # MCP resources
│   │   └── bill_resources.py       # Bill document access
│   └── utils/                       # Utilities
│       ├── formatters.py           # Date/biennium formatting
│       └── bill_document_utils.py  # Document helpers
├── tests/                           # 444 tests (380+ unit, 64+ property)
│   ├── property/                    # Property-based tests
│   │   └── test_*.py               # 64+ property tests
│   └── test_*.py                    # 380+ unit tests
├── pyproject.toml                   # Dependencies and config
├── Makefile                         # Development commands
└── README.md
```

## Development

### Setting Up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/awalcutt/wa-leg-mcp.git
cd wa-leg-mcp
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
make test
```

### Adding New Tools

1. Create a new file in `src/wa_leg_mcp/tools/`
2. Implement tool using the MCP decorator:
```python
from mcp.server.fastmcp import Tool

@Tool("toolName", description="Tool description")
def tool_function(param1: str, param2: str = None):
    # Implementation
    return {"result": data}
```

3. Register tool in server.py by adding it to the `get_default_tools()` function
4. Add tests in `tests/`

## Deployment Options

### Local Deployment
- Run directly with Python
- Use with MCP Inspector for development

### Cloud Deployment
- AWS Lambda with API Gateway (supports remote connections via `mcp-remote` adapter)
- Google Cloud Functions
- Azure Functions

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WSL_API_TIMEOUT` | API request timeout (seconds) | 30 |
| `WSL_CACHE_TTL` | Cache time-to-live (seconds) | 300 |
| `LOG_LEVEL` | Logging level | INFO |
| `SERVER_NAME` | Custom server name | Washington State Legislature MCP Server |

## Usage Examples

### With Claude Desktop
Add to Claude Desktop configuration:
```json
{
  "mcpServers": {
    "wa-leg": {
      "command": "python",
      "args": ["path/to/src/wa_leg_mcp/server.py"],
      "env": {
        "WSL_CACHE_TTL": "600"
      }
    }
  }
}
```

### With Other AI Clients
```python
# Example client integration
from mcp.client import ClientSession
import asyncio

async def connect_to_legislature_mcp():
    async with ClientSession(server_command=["python", "src/wa_leg_mcp/server.py"]) as session:
        # List available tools
        tools = await session.list_tools()
        
        # Call a tool
        result = await session.call_tool("getBillInfo", {
            "bill_number": "HB1234",
            "biennium": "2025-26"
        })
        
        print(result)
        
        # Access a resource
        bill_xml = await session.read_resource(
            "bill://xml/2025-26/House/1234"
        )
        
        print(f"Bill XML content length: {len(bill_xml)}")

asyncio.run(connect_to_legislature_mcp())
```

## API Documentation

### Tools

#### getBillInfo
Retrieves detailed information about a specific bill using the GetLegislation API.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234", "SB5678")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: Bill details including description, sponsor, status, fiscal notes, and companions

#### searchBills
Searches for bills using keywords and optional filtering via the WSL Search API.

Parameters:
- `query` (string, required): Search query text (e.g., "climate change", "transportation")
- `bienniums` (array, optional): List of bienniums to search (format: "YYYY-YY"), defaults to current
- `agency` (string, optional): Filter by originating agency ("House", "Senate", or "Both")
- `max_results` (integer, optional): Maximum number of total results to return (max 100)

Returns: List of bills matching the search criteria

#### getBillsByYear
Retrieves all bills from a specific year with optional filtering using the GetLegislationByYear API.

Parameters:
- `year` (string, optional): Year in format "YYYY" (e.g., "2025"), defaults to current
- `agency` (string, optional): Filter by originating agency ("House" or "Senate")
- `active_only` (boolean, optional): If True, only return active bills

Returns: List of bills matching the criteria

#### getCommitteeMeetings
Retrieves committee meetings and agendas using the GetCommitteeMeetings API.

Parameters:
- `start_date` (string, required): Start date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format
- `committee` (string, optional): Filter by specific committee

Returns: List of committee meetings with dates, times, locations, and agenda items

#### findLegislator
Finds legislators using the GetSponsors API.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `chamber` (string, optional): "house" or "senate"

Returns: List of legislators with ID, name, party, and contact information

#### getBillStatus
Gets current status and history using the GetCurrentStatus API.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: Current status, history, action dates, and status descriptions

#### getBillDocuments
Retrieves bill documents metadata (functionality based on Document service endpoints).

Parameters:
- `bill_number` (string, required): Bill number
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `document_type` (string, optional): "bill", "amendment", "report"

Returns: Document metadata with links to HTML and PDF versions

#### getBillContent
Retrieves the actual content of a bill in an AI-friendly format.

Parameters:
- `bill_number` (integer, required): Bill number as an integer (e.g., 1234 for HB1234)
- `biennium` (string, optional): Legislative biennium in format "2025-26" (defaults to current)
- `chamber` (string, optional): Chamber name - "House" or "Senate" (optional if bill_number is unique across chambers)
- `bill_format` (string, optional): Document format - "xml" (default), "htm", or "pdf"

Returns: For XML and HTM formats: Dict containing the document content and metadata. For PDF format: Dict containing the URL to access the PDF and metadata.

#### getRollCalls
Get roll call voting records for a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234", "SB5678")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: Roll call votes with legislator names, vote values (yea/nay/absent/excused), and vote dates

#### getAmendmentsForBiennium
Get amendments for a bill in a biennium.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of amendments with sponsor, description, and status

#### getAmendmentsForYear
Get amendments for a bill in a specific year.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `year` (string, required): Year in format "YYYY" or "YY" (e.g., "2025" or "25")

Returns: List of amendments for the specified year

#### getHearings
Get committee hearings for a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of hearings with committee, date, time, location, and agenda items

#### getRcwCitesAffected
Get RCW sections affected by a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of RCW citations with section numbers and action types (amended, repealed, created)

#### getSessionLawByBill
Get session law information for a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: Session law with chapter number, effective date, and law text reference

#### getSessionLawByBillId
Get session law by bill ID.

Parameters:
- `bill_id` (string, required): Bill ID (e.g., "HB 1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: Session law information

#### getBillByChapterNumber
Get bill information by session law chapter number.

Parameters:
- `year` (integer, required): Year (e.g., 2025)
- `session` (integer, required): Session code (0=Regular, 1=1st Special, etc.)
- `chapter_number` (integer, required): Chapter number

Returns: Bill information for the specified chapter

#### getChapterNumbersByYear
Get all session law chapters for a year.

Parameters:
- `year` (integer, required): Year (e.g., 2025)

Returns: List of all session law chapters enacted that year

#### getSessionLawByInitiativeNumber
Get session law for an initiative.

Parameters:
- `initiative_number` (integer, required): Initiative number (e.g., 1234 for I-1234)

Returns: Initiative session law information

#### getLegislationGovernorSigned
Get bills signed by the governor.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of signed bills with action dates

#### getLegislationGovernorVeto
Get bills vetoed by the governor.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of vetoed bills with veto messages

#### getLegislationGovernorPartialVeto
Get bills with line-item vetoes by the governor.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of partially vetoed bills with affected sections

#### getCommitteeExecutiveActionsByBill
Get executive actions taken on a bill by committees.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of executive actions with committee, date, and action type

#### getCommitteeReferralsByBill
Get committee referrals for a bill.

Parameters:
- `bill_number` (string, required): Bill number (e.g., "HB1234")
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of referrals with committees and dates

#### getCommitteeReferralsByCommittee
Get bills referred to a specific committee.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `committee_name` (string, required): Committee name (e.g., "House Finance")

Returns: List of bills referred to the committee

#### getDoPassByCommittee
Get bills with "do pass" recommendation from a committee.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `committee_name` (string, required): Committee name

Returns: List of bills that received do pass recommendation

#### getInCommittee
Get bills currently in a committee.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `committee_name` (string, required): Committee name

Returns: List of bills currently referred to the committee

#### getLegislationReportedOutOfCommittee
Get bills reported out of a committee.

Parameters:
- `committee_name` (string, required): Committee name
- `begin_date` (string, required): Begin date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format

Returns: List of bills reported out with recommendation type and vote counts

#### getActiveCommittees
Get all currently active committees.

Parameters: None

Returns: List of active committees for both House and Senate

#### getActiveHouseCommittees
Get active House committees.

Parameters: None

Returns: List of active House committees

#### getActiveSenateCommittees
Get active Senate committees.

Parameters: None

Returns: List of active Senate committees

#### getActiveCommitteeMembers
Get members of an active committee.

Parameters:
- `committee_name` (string, required): Committee name

Returns: List of members with names, roles, party, district, and contact information

#### getCommitteeMembers
Get committee members for a biennium (historical).

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `committee_name` (string, required): Committee name

Returns: List of committee members for the specified biennium

#### getHouseCommittees
Get all House committees for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of House committees

#### getSenateCommittees
Get all Senate committees for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of Senate committees

#### getSponsors
Get all sponsors for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of sponsors for both chambers with contact information

#### getHouseSponsors
Get House sponsors.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of House sponsors

#### getSenateSponors
Get Senate sponsors.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of Senate sponsors

#### getRequesters
Get entities authorized to request legislation.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of requesters

#### getLegislationPassedHouse
Get bills that passed the House.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of House-passed bills with passage dates and vote counts

#### getLegislationPassedSenate
Get bills that passed the Senate.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of Senate-passed bills with passage dates and vote counts

#### getLegislationPassedLegislature
Get bills that passed both chambers.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of bills that passed both House and Senate

#### getPrefiledLegislation
Get prefiled bills.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of prefiled bills with filing dates and sponsors

#### getLegislativeStatusChanges
Get bill status changes in a date range.

Parameters:
- `begin_date` (string, required): Begin date in YYYY-MM-DD format
- `end_date` (string, required): End date in YYYY-MM-DD format
- `biennium` (string, optional): Filter by biennium

Returns: List of status changes with old/new status and dates

#### getDocumentClasses
Get available document types for a biennium.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"

Returns: List of document classes with names and descriptions

#### getAllDocumentsByClass
Get all documents of a specific class.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `document_class` (string, required): Document class (e.g., "Bills", "Amendments")

Returns: List of documents with names, URLs, and bill associations

#### getDocumentsByClass
Get documents by class with name filter.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `document_class` (string, required): Document class
- `name_filter` (string, required): Pattern to match (e.g., "HB 1*")

Returns: List of filtered documents

#### getLegislationTypes
Get valid legislation types.

Parameters: None (results cached for 24 hours)

Returns: List of legislation type codes and descriptions

#### getLegislationByRequestNumber
Look up bill by request number.

Parameters:
- `biennium` (string, required): Legislative biennium in format "2025-26"
- `request_number` (string, required): Request number (e.g., "23-1234")

Returns: Bill information or request status

#### getRevisedCommitteeMeetings
Get committee meetings revised since a date.

Parameters:
- `since_date` (string, required): Date in YYYY-MM-DD format
- `biennium` (string, optional): Filter by biennium

Returns: List of revised meetings

### Resources

#### Bill Document Resources
The MCP server provides direct access to bill documents through URI templates:

##### bill://xml/{biennium}/{chamber}/{bill_number}
Access bill documents in structured XML format (recommended for AI processing).

Parameters:
- `biennium` (string): Legislative biennium in format "YYYY-YY" (e.g., "2025-26")
- `chamber` (string): Chamber name - must be exactly "House" or "Senate"
- `bill_number` (string): Bill number as numeric string (e.g., "1234")

Returns: XML content of the bill document

##### bill://htm/{biennium}/{chamber}/{bill_number}
Access bill documents in HTML format with hyperlinks to referenced laws.

Parameters:
- `biennium` (string): Legislative biennium in format "YYYY-YY"
- `chamber` (string): "House" or "Senate"
- `bill_number` (string): Bill number

Returns: HTML content of the bill document

##### bill://pdf/{biennium}/{chamber}/{bill_number}
Get URLs for bill PDF documents (content not fetched).

Parameters:
- `biennium` (string): Legislative biennium in format "YYYY-YY"
- `chamber` (string): "House" or "Senate"
- `bill_number` (string): Bill number

Returns: Dictionary with URL to access the PDF document

##### bill://document/{format}/{biennium}/{chamber}/{bill_number}
Generic format for accessing bill documents in any supported format.

Parameters:
- `format` (string): Document format - "xml", "htm", or "pdf"
- `biennium` (string): Legislative biennium in format "YYYY-YY"
- `chamber` (string): "House" or "Senate"
- `bill_number` (string): Bill number

Returns: Document content or URL based on format

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
