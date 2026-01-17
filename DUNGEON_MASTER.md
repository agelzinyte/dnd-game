# AI Dungeon Master Feature

The DungeonMaster class uses OpenAI's API to provide dynamic, AI-generated narration for your D&D game.

## Setup

### 1. Get an OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again!)

### 2. Configure Your API Key

Open the [.env](.env) file in the project root and replace `your_api_key_here` with your actual API key:

```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Important:** Never commit your `.env` file to git! It's already in `.gitignore` to prevent this.

### 3. Install Dependencies

The required dependencies (`python-dotenv` and `openai`) are already in [requirements.txt](requirements.txt).

Install them with:
```bash
uv pip install python-dotenv openai
```

Or install all dependencies:
```bash
uv pip install -r requirements.txt
```

## Usage

When you start the game, you'll be asked if you want to enable DM narration:

```
Do you want AI Dungeon Master narration? (Requires OpenAI API key)
1. Yes, enable DM narration
2. No, play without narration
```

### With DM Narration Enabled

The DM will narrate:
- **Combat starts**: Atmospheric description of the encounter
- **Your turn**: What actions are available
- **Weapon attacks**: Vivid descriptions of hits and misses
- **Spell casting**: Magical narration of spells
- **Enemy attacks**: Dramatic descriptions of enemy actions
- **Victory/Defeat**: Epic conclusions to battles

Example narration:
```
🎲 The shadows of the dungeon seem to coalesce into form as a
snarling Goblin emerges, brandishing a crude blade with malicious intent.

🎲 What will Aragorn do in this tense moment—will they attack with
their weapon, cast a spell, or run away?

🎲 Aragorn's blade flashes through the air, striking true! The Goblin
staggers back as steel bites deep, crimson blood marking the hit.
```

### Without DM Narration

The game plays normally without any AI narration, using only the standard combat messages.

## Model Selection

The DungeonMaster uses `gpt-4o-mini` by default for cost efficiency. This model provides good narration at lower costs.

You can change the model in [dndgame/dungeon_master.py](dndgame/dungeon_master.py):

```python
dm = DungeonMaster(model="gpt-4o")  # Use a more powerful model
```

## Cost Considerations

- **gpt-4o-mini** (default): ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- Each narration uses approximately 50-150 tokens
- A typical combat might use 500-1000 tokens total (~$0.001 per combat)

## Troubleshooting

### "Warning: OpenAI API key not configured"

This means:
- Your `.env` file doesn't exist, or
- Your API key is still set to `your_api_key_here`, or
- Your API key is invalid

**Solution:** Check your `.env` file and ensure you've added a valid API key.

### API Errors During Narration

If the API call fails:
- The game will display a warning message
- The game will continue without narration for that action
- Check your internet connection
- Verify your API key is valid and has available credits

### Import Errors

If you see `ModuleNotFoundError: No module named 'openai'` or similar:

**Solution:** Install the required dependencies:
```bash
uv pip install -r requirements.txt
```

## Features

### Implemented Narration

- ✅ Combat encounter starts
- ✅ Player action choices
- ✅ Weapon attacks (hits and misses)
- ✅ Spell casting
- ✅ Enemy attacks
- ✅ Victory narration
- ✅ Defeat narration

### Safety Features

- Graceful fallback if API key is missing
- Error handling for API failures
- Game continues even if narration fails
- Option to disable narration entirely

## Technical Details

The DungeonMaster class is located in [dndgame/dungeon_master.py](dndgame/dungeon_master.py).

Key methods:
- `narrate_combat_start()`: Narrates the beginning of combat
- `narrate_attack()`: Narrates weapon attacks
- `narrate_spell_cast()`: Narrates spell casting
- `narrate_victory()`: Narrates player victory
- `narrate_defeat()`: Narrates player defeat
- `narrate_action_choice()`: Narrates available actions

All methods return `None` if narration is disabled, allowing the game to continue normally.
