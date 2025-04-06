# Event System Documentation

## Overview

The Event System is a flexible and extensible framework for managing in-game events in a fantasy world simulation. It consists of three main components:
1. Event Definitions (JSON)
2. Event Processor (Python)
3. Common Conditions

## Event Definitions

Event definitions are stored in `data/event_definitions.json`. Each event follows this structure:

```json
{
  "events": {
    "category_name": {
      "event_id": {
        "name": "Event Name",
        "conditions": [
          {
            "type": "condition_type",
            "operator": "comparison_operator",
            "value": "condition_value"
          }
        ],
        "effects": [
          {
            "type": "effect_type",
            "parameters": {}
          }
        ],
        "followup_events": [
          {
            "id": "followup_event_id",
            "delay": delay_in_years,
            "probability": probability_value
          }
        ],
        "is_followup": false
      }
    }
  }
}
```

### Categories

Events are organized into categories (e.g., natural, magical, political) for better organization and processing.

### Condition Types

- `year`: Checks the current year
- `season`: Checks the current season
- `faction`: Checks faction statistics
- `region`: Checks region statistics
- `common`: Uses a predefined common condition

### Operators

- `==`: Equal to
- `!=`: Not equal to
- `>`: Greater than
- `>=`: Greater than or equal to
- `<`: Less than
- `<=`: Less than or equal to

### Effect Types

- `modify_stat`: Modifies a statistic value
- `change_leader`: Changes a faction's leader

## Common Conditions

Common conditions are reusable condition blocks:

```json
{
  "realm_in_crisis": {
    "type": "faction",
    "faction": "Noble Houses",
    "stat": "stability",
    "operator": "<=",
    "value": 30
  },
  "magical_instability": {
    "type": "region",
    "region": "Central Valley",
    "stat": "magical_energy",
    "operator": ">=",
    "value": 80
  }
}
```

## Causal Chains

Events can trigger follow-up events:

```json
"followup_events": [
  {
    "id": "followup_event_id",
    "delay": 1,
    "probability": 0.3
  }
]
```

- `delay`: Delay in years before the event triggers (must be a number)
- `probability`: Probability of the event triggering (must be between 0.0 and 1.0)
- `is_followup`: Boolean flag indicating if this is a follow-up event

## Validation

The system validates:
- Presence of all required fields
- Correct structure of conditions and effects
- Existence of referenced events
- Validity of operators and values
- Type correctness of values (e.g., delay must be numeric)
- Probability values (must be between 0 and 1)
- Structure of follow-up events

## Extending the System

To add new events:
1. Choose an appropriate category (natural, magical, political)
2. Define a unique ID and name
3. Specify conditions and effects
4. Add follow-up events if needed
5. Test the validation

## Examples

### Natural Event
```json
{
  "events": {
    "natural": {
      "dragon_migration": {
        "name": "Dragon Migration",
        "conditions": [
          {
            "type": "year",
            "operator": ">=",
            "value": 1000
          },
          {
            "type": "season",
            "operator": "==",
            "value": "autumn"
          }
        ],
        "effects": [
          {
            "type": "modify_stat",
            "region": "Northern Mountains",
            "stat": "dragon_activity",
            "value": 20
          }
        ],
        "is_followup": false
      }
    }
  }
}
```

### Political Event
```json
{
  "events": {
    "political": {
      "mages_guild_coup": {
        "name": "Mages' Guild Coup",
        "conditions": [
          {
            "type": "common",
            "value": "magical_instability"
          }
        ],
        "effects": [
          {
            "type": "change_leader",
            "faction": "Mages' Guild",
            "new_leader": "Archmage Varis"
          }
        ],
        "is_followup": false
      }
    }
  }
}
```

## Best Practices

1. **Naming Conventions**
   - Use descriptive, unique IDs
   - Keep names clear and concise
   - Follow consistent naming patterns

2. **Condition Design**
   - Use common conditions for frequently used checks
   - Keep conditions simple and focused
   - Consider performance implications

3. **Effect Design**
   - Make effects atomic and focused
   - Consider balance implications
   - Document complex effects

4. **Follow-up Events**
   - Use appropriate delays
   - Set reasonable probabilities
   - Consider event chains carefully
   - Mark follow-up events with `is_followup: true`

## Troubleshooting

Common issues and solutions:

1. **Event Not Triggering**
   - Check condition values
   - Verify operator usage
   - Check world state values

2. **Invalid Event Structure**
   - Run validation
   - Check required fields
   - Verify JSON syntax
   - Ensure proper category structure

3. **Unexpected Effects**
   - Review effect parameters
   - Check value ranges
   - Verify world state updates 