#!/usr/bin/env python3
"""
Weekly D&D Character Sheet Updater
Updates character data and regenerates fresh sheets
"""

import json
import os
from datetime import datetime
from simple_sheet_generator import generate_html_sheet, load_kazrek_data

def update_character_data(updates):
    """Update character data with weekly changes"""
    char_data = load_kazrek_data()
    
    # Update XP
    if 'xp_gained' in updates:
        current_xp = char_data.get('current_xp', 0)
        if isinstance(current_xp, str):
            current_xp = int(current_xp) if current_xp.isdigit() else 0
        char_data['current_xp'] = current_xp + updates['xp_gained']
        
        # Check for level up
        if char_data['current_xp'] >= 900 and char_data['level'] < 3:
            char_data = level_up_to_3(char_data)
    
    # Update HP
    if 'current_hp' in updates:
        char_data['current_hp'] = updates['current_hp']
    
    # Add equipment
    if 'new_equipment' in updates:
        char_data['equipment'].extend(updates['new_equipment'])
    
    # Update currency
    if 'currency_changes' in updates:
        for coin_type, amount in updates['currency_changes'].items():
            char_data['currency'][coin_type] = char_data['currency'].get(coin_type, 0) + amount
    
    # Add session info
    char_data['session'] = updates.get('session_number', char_data.get('session', 'Unknown'))
    char_data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    return char_data

def level_up_to_3(char_data):
    """Level up character to level 3"""
    char_data['level'] = 3
    char_data['next_level_xp'] = '2700'
    
    # Update HP (roll or average)
    new_hp = input("Level 3 HP gain - Enter roll result (1-6) or press Enter for average (4): ").strip()
    if new_hp.isdigit() and 1 <= int(new_hp) <= 6:
        hp_gain = int(new_hp) + 4  # Con modifier
    else:
        hp_gain = 8  # Average 4 + 4 Con
    
    char_data['hp_max'] += hp_gain
    
    # Add sorcery point
    char_data['sorcery_points'] = 3
    
    # Add 2nd level spell slots
    char_data['spell_slots']['2nd'] = 2
    
    # Add new spell
    print("\nLevel 3 - Learn a new spell!")
    print("Available 1st or 2nd level spells:")
    print("1. Misty Step (2nd) - Teleport 30 feet")
    print("2. Web (2nd) - Restrain enemies in 20ft cube") 
    print("3. Mirror Image (2nd) - Create 3 duplicates")
    print("4. Detect Magic (1st) - See magical auras")
    print("5. Sleep (1st) - Put creatures to sleep")
    
    choice = input("Enter spell choice (1-5): ").strip()
    spell_choices = {
        '1': ('2nd', 'Misty Step'),
        '2': ('2nd', 'Web'),
        '3': ('2nd', 'Mirror Image'),
        '4': ('1st', 'Detect Magic'),
        '5': ('1st', 'Sleep')
    }
    
    if choice in spell_choices:
        level, spell = spell_choices[choice]
        if level not in char_data['spells']:
            char_data['spells'][level] = []
        char_data['spells'][level].append(spell)
    
    # Add Metamagic
    print("\nChoose 2 Metamagic options:")
    print("1. Subtle Spell - Cast without somatic/verbal components")
    print("2. Twinned Spell - Target second creature with single-target spell")
    print("3. Quickened Spell - Cast spell as bonus action")
    print("4. Empowered Spell - Reroll damage dice")
    
    meta1 = input("First metamagic choice (1-4): ").strip()
    meta2 = input("Second metamagic choice (1-4): ").strip()
    
    metamagic_options = {
        '1': 'Subtle Spell',
        '2': 'Twinned Spell', 
        '3': 'Quickened Spell',
        '4': 'Empowered Spell'
    }
    
    char_data['metamagic'] = []
    if meta1 in metamagic_options:
        char_data['metamagic'].append(metamagic_options[meta1])
    if meta2 in metamagic_options and meta2 != meta1:
        char_data['metamagic'].append(metamagic_options[meta2])
    
    print(f"\\n🎉 LEVEL UP! Kazrek is now Level 3!")
    print(f"New HP Max: {char_data['hp_max']}")
    print(f"Sorcery Points: {char_data['sorcery_points']}")
    print(f"New Spells: {char_data.get('metamagic', [])}")
    
    return char_data

def interactive_update():
    """Interactive session update"""
    print("=== KAZREK SPELLFORGE - WEEKLY UPDATE ===")
    print()
    
    updates = {}
    
    # Session info
    session_num = input("Session number: ").strip()
    if session_num:
        updates['session_number'] = session_num
    
    # XP
    xp_gained = input("XP gained this session (or 0): ").strip()
    if xp_gained.isdigit():
        updates['xp_gained'] = int(xp_gained)
    
    # Current HP
    current_hp = input("Current HP after session (or press Enter to skip): ").strip()
    if current_hp.isdigit():
        updates['current_hp'] = int(current_hp)
    
    # Equipment
    print("\\nNew equipment (one item per line, empty line when done):")
    new_equipment = []
    while True:
        item = input("Item: ").strip()
        if not item:
            break
        new_equipment.append(item)
    if new_equipment:
        updates['new_equipment'] = new_equipment
    
    # Currency changes
    print("\\nCurrency changes:")
    currency_changes = {}
    
    for coin_type in ['cp', 'sp', 'gp']:
        change = input(f"{coin_type.upper()} gained/lost (+/-): ").strip()
        if change and (change.startswith('+') or change.startswith('-')) and change[1:].isdigit():
            currency_changes[coin_type] = int(change)
    
    if currency_changes:
        updates['currency_changes'] = currency_changes
    
    return updates

def save_character_data(char_data, filename="kazrek_data.json"):
    """Save character data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(char_data, f, indent=2)
    print(f"📁 Character data saved to {filename}")

def generate_session_summary(char_data, updates):
    """Generate session summary"""
    summary = f"""
=== SESSION {char_data.get('session', 'N/A')} SUMMARY ===
Date: {datetime.now().strftime('%B %d, %Y')}
Character: {char_data['name']} (Level {char_data['level']})

XP: {updates.get('xp_gained', 0)} gained
New Equipment: {', '.join(updates.get('new_equipment', ['None']))}
Currency Changes: {', '.join([f"{v:+d} {k}" for k, v in updates.get('currency_changes', {}).items()])}

Current Stats:
- HP: {char_data.get('current_hp', '?')} / {char_data['hp_max']}
- XP: {char_data.get('current_xp', '?')} / {char_data['next_level_xp']}
- Gold: {char_data['currency'].get('gp', 0)} gp

Files Generated:
- Kazrek_Official_Sheet.html (printable character sheet)
- kazrek_data.json (character data backup)
"""
    
    with open(f"session_{char_data.get('session', 'X')}_summary.txt", 'w') as f:
        f.write(summary)
    
    print(summary)

if __name__ == "__main__":
    try:
        # Get updates from user
        updates = interactive_update()
        
        if not updates:
            print("No updates provided. Exiting.")
            exit()
        
        # Update character data
        print("\\n🔄 Updating character data...")
        char_data = update_character_data(updates)
        
        # Save updated data
        save_character_data(char_data)
        
        # Generate new character sheet
        print("📄 Generating new character sheet...")
        generate_html_sheet(char_data, "Kazrek_Official_Sheet.html")
        
        # Generate session summary
        generate_session_summary(char_data, updates)
        
        print("\\n✅ Update complete! Files ready for next session:")
        print("  📋 Kazrek_Official_Sheet.html (open in browser, print to PDF)")
        print("  📁 kazrek_data.json (character data backup)")
        print(f"  📝 session_{char_data.get('session', 'X')}_summary.txt (session recap)")
        
    except KeyboardInterrupt:
        print("\\n\\nUpdate cancelled.")
    except Exception as e:
        print(f"\\n❌ Error during update: {e}")
        print("Please check your inputs and try again.")