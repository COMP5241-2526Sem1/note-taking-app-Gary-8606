"""
Note Templates functionality for predefined note structures
"""

# Predefined note templates
NOTE_TEMPLATES = {
    "meeting": {
        "title": "Meeting Notes - {date}",
        "content": """## Meeting Details
**Date:** {date}
**Time:** 
**Attendees:** 
**Location/Platform:** 

## Agenda
1. 
2. 
3. 

## Discussion Points
- 
- 
- 

## Action Items
- [ ] Task 1 - Assigned to: 
- [ ] Task 2 - Assigned to: 
- [ ] Task 3 - Assigned to: 

## Next Steps
- 
- 

## Additional Notes
""",
        "tags": ["meeting", "work", "notes"]
    },
    
    "project": {
        "title": "Project Plan - {title}",
        "content": """## Project Overview
**Project Name:** 
**Start Date:** {date}
**End Date:** 
**Project Manager:** 
**Team Members:** 

## Objectives
- 
- 
- 

## Scope
### In Scope
- 
- 

### Out of Scope
- 
- 

## Timeline & Milestones
- [ ] Milestone 1 - Due: 
- [ ] Milestone 2 - Due: 
- [ ] Milestone 3 - Due: 

## Resources Required
- **Personnel:** 
- **Budget:** 
- **Tools/Software:** 
- **Hardware:** 

## Risk Assessment
- **Risk 1:** 
  - Impact: 
  - Mitigation: 
- **Risk 2:** 
  - Impact: 
  - Mitigation: 

## Success Criteria
- 
- 
- 
""",
        "tags": ["project", "planning", "work"]
    },
    
    "daily_journal": {
        "title": "Daily Journal - {date}",
        "content": """## {date} - Daily Reflection

### Today's Priorities
1. 
2. 
3. 

### Accomplishments
✅ 
✅ 
✅ 

### Challenges Faced
- 
- 

### Lessons Learned
- 
- 

### Gratitude
- 
- 
- 

### Tomorrow's Goals
- [ ] 
- [ ] 
- [ ] 

### Mood: 😊 😐 😔
Rate your day: ⭐⭐⭐⭐⭐

### Notes & Reflections
""",
        "tags": ["journal", "personal", "reflection"]
    },
    
    "research": {
        "title": "Research Notes - {title}",
        "content": """## Research Topic: 

### Research Question
What am I trying to find out?

### Sources
1. **Source 1:** 
   - Author: 
   - Date: 
   - URL/Reference: 
   - Key Points: 
   
2. **Source 2:** 
   - Author: 
   - Date: 
   - URL/Reference: 
   - Key Points: 

### Key Findings
- 
- 
- 

### Quotes & Citations
> "Quote 1" - Author, Year

> "Quote 2" - Author, Year

### Analysis
- 
- 
- 

### Questions for Further Research
- 
- 

### Next Steps
- [ ] 
- [ ] 
- [ ] 
""",
        "tags": ["research", "study", "academic"]
    },
    
    "book_review": {
        "title": "Book Review - {title}",
        "content": """## Book Information
**Title:** 
**Author:** 
**Genre:** 
**Publication Year:** 
**Pages:** 
**Rating:** ⭐⭐⭐⭐⭐

## Summary
Brief overview of the book's main points or plot:

## Key Takeaways
- 
- 
- 

## Favorite Quotes
> "Quote 1"

> "Quote 2"

## What I Liked
- 
- 
- 

## What I Didn't Like
- 
- 

## Who Should Read This
This book is perfect for:
- 
- 

## Personal Reflection
How this book impacted me:

## Related Books/Next Reading
- 
- 
""",
        "tags": ["book", "review", "reading"]
    },
    
    "travel_plan": {
        "title": "Travel Itinerary - {title}",
        "content": """## Trip Overview
**Destination:** 
**Dates:** {date} - 
**Duration:** 
**Travelers:** 
**Budget:** 

## Pre-Trip Checklist
- [ ] Book flights
- [ ] Reserve accommodation
- [ ] Get travel insurance
- [ ] Check passport/visa requirements
- [ ] Pack essentials
- [ ] Arrange pet/house sitting
- [ ] Set up international phone plan

## Itinerary
### Day 1 - {date}
- **Morning:** 
- **Afternoon:** 
- **Evening:** 

### Day 2
- **Morning:** 
- **Afternoon:** 
- **Evening:** 

## Accommodations
- **Hotel/Airbnb:** 
- **Address:** 
- **Check-in:** 
- **Check-out:** 
- **Confirmation:** 

## Transportation
- **Flights:** 
- **Local Transport:** 
- **Car Rental:** 

## Must-See Attractions
- 
- 
- 

## Restaurants to Try
- 
- 
- 

## Emergency Contacts
- **Embassy:** 
- **Local Emergency:** 
- **Insurance:** 

## Budget Breakdown
- **Flights:** $
- **Accommodation:** $
- **Food:** $
- **Activities:** $
- **Transportation:** $
- **Total:** $
""",
        "tags": ["travel", "planning", "itinerary"]
    }
}

def get_template_list():
    """Return list of available templates with descriptions"""
    return [
        {
            "id": "meeting",
            "name": "Meeting Notes",
            "description": "Structured template for meeting notes with agenda, action items, and follow-ups",
            "icon": "👥"
        },
        {
            "id": "project", 
            "name": "Project Planning",
            "description": "Comprehensive project planning template with objectives, timeline, and risk assessment",
            "icon": "📋"
        },
        {
            "id": "daily_journal",
            "name": "Daily Journal",
            "description": "Personal reflection template for daily journaling and goal setting",
            "icon": "📔"
        },
        {
            "id": "research",
            "name": "Research Notes", 
            "description": "Academic research template with sources, citations, and analysis",
            "icon": "🔍"
        },
        {
            "id": "book_review",
            "name": "Book Review",
            "description": "Book review template with ratings, quotes, and personal reflections",
            "icon": "📚"
        },
        {
            "id": "travel_plan",
            "name": "Travel Itinerary",
            "description": "Complete travel planning template with itinerary, budget, and checklists",
            "icon": "✈️"
        }
    ]

def get_template(template_id):
    """Get a specific template by ID"""
    return NOTE_TEMPLATES.get(template_id)

def format_template(template_id, **kwargs):
    """Format a template with provided variables"""
    template = NOTE_TEMPLATES.get(template_id)
    if not template:
        return None
    
    # Default values
    from datetime import datetime
    defaults = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'title': 'New Note'
    }
    defaults.update(kwargs)
    
    try:
        formatted_template = {
            'title': template['title'].format(**defaults),
            'content': template['content'].format(**defaults),
            'tags': template['tags']
        }
        return formatted_template
    except KeyError as e:
        # If formatting fails, return template without formatting
        return template