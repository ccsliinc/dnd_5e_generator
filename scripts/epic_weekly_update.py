#!/usr/bin/env python3
"""
Epic Weekly D&D Character Sheet Updater
Updates character data and regenerates stunning modern sheets
"""

import json
import os
from datetime import datetime
from modern_sheet_generator import generate_modern_sheet, load_kazrek_data

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
            print("🎉 LEVEL UP DETECTED! Kazrek is ready for Level 3!")
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
    """Level up character to level 3 with full Sorcerer features"""
    print("\n" + "="*50)
    print("🌟 SORCERER LEVEL 3 ADVANCEMENT 🌟")
    print("="*50)
    
    char_data['level'] = 3
    char_data['next_level_xp'] = '2700'
    
    # Update HP (roll or average)
    print("\n💚 HIT POINTS:")
    new_hp = input("Roll 1d6 for HP (1-6) or press Enter for average (4): ").strip()
    if new_hp.isdigit() and 1 <= int(new_hp) <= 6:
        hp_gain = int(new_hp) + 4  # Con modifier
        print(f"Rolled {new_hp}! +{hp_gain} HP (including +4 Con)")
    else:
        hp_gain = 8  # Average 4 + 4 Con
        print("Taking average: +8 HP")
    
    char_data['hp_max'] += hp_gain
    print(f"New Max HP: {char_data['hp_max']}")
    
    # Add sorcery point
    char_data['sorcery_points'] = 3
    print(f"\n🔮 SORCERY POINTS: Now have {char_data['sorcery_points']} points")
    
    # Add 2nd level spell slots
    char_data['spell_slots']['2nd'] = 2
    print("✨ SPELL SLOTS: Gained 2nd level slots (2 slots)")
    
    # Add new spell
    print("\n📚 LEARN NEW SPELL:")
    print("Choose 1 spell (1st or 2nd level):")
    print("1. 🔥 Misty Step (2nd) - Teleport 30 feet as bonus action")
    print("2. 🕷️  Web (2nd) - Restrain enemies in 20ft cube, Dex save")
    print("3. 🪞 Mirror Image (2nd) - Create 3 duplicates, confuse attackers")
    print("4. 🔍 Detect Magic (1st) - See magical auras for 10 minutes")
    print("5. 😴 Sleep (1st) - Put 5d8+5 HP worth of creatures to sleep")
    
    choice = input("\\nEnter spell choice (1-5): ").strip()
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
        print(f"✅ Learned: {spell} ({level} level)")
    else:
        print("⚠️  Invalid choice, defaulting to Misty Step")
        if '2nd' not in char_data['spells']:
            char_data['spells']['2nd'] = []
        char_data['spells']['2nd'].append('Misty Step')
    
    # Add Metamagic
    print("\\n🌟 METAMAGIC OPTIONS:")
    print("Choose 2 metamagic options to customize your spells:")
    print("1. 🤫 Subtle Spell (1 SP) - Cast without somatic/verbal components")
    print("2. ⚡ Twinned Spell (SP = spell level) - Target second creature")
    print("3. 💨 Quickened Spell (2 SP) - Cast spell as bonus action")
    print("4. 🎲 Empowered Spell (1 SP) - Reroll damage dice")
    
    meta1 = input("\\nFirst metamagic choice (1-4): ").strip()
    meta2 = input("Second metamagic choice (1-4, different from first): ").strip()
    
    metamagic_options = {
        '1': 'Subtle Spell',
        '2': 'Twinned Spell', 
        '3': 'Quickened Spell',
        '4': 'Empowered Spell'
    }
    
    char_data['metamagic'] = []
    if meta1 in metamagic_options:
        char_data['metamagic'].append(metamagic_options[meta1])
        print(f"✅ Gained: {metamagic_options[meta1]}")
    if meta2 in metamagic_options and meta2 != meta1:
        char_data['metamagic'].append(metamagic_options[meta2])
        print(f"✅ Gained: {metamagic_options[meta2]}")
    
    if len(char_data['metamagic']) < 2:
        print("⚠️  Incomplete selection, adding Subtle Spell + Twinned Spell")
        char_data['metamagic'] = ['Subtle Spell', 'Twinned Spell']
    
    print("\\n" + "="*50)
    print("🎉 LEVEL 3 SORCERER COMPLETE! 🎉")
    print("="*50)
    print(f"HP: {char_data['hp_max']} (gained +{hp_gain})")
    print(f"Sorcery Points: {char_data['sorcery_points']}")
    print(f"New Spells: {char_data['spells'].get('2nd', []) + char_data['spells'].get('1st', [])[2:]}")  # New spells only
    print(f"Metamagic: {', '.join(char_data['metamagic'])}")
    print("2nd Level Spell Slots: 2")
    print("\\n🐉 Ready for more powerful magic!")
    
    return char_data

def interactive_update():
    """Interactive session update with style"""
    print("🎨" + "="*60 + "🎨")
    print("✨      KAZREK SPELLFORGE - EPIC SESSION UPDATE      ✨")
    print("🎨" + "="*60 + "🎨")
    print()
    
    updates = {}
    
    # Session info
    print("📅 SESSION INFORMATION:")
    session_num = input("Session number: ").strip()
    if session_num:
        updates['session_number'] = session_num
        print(f"✅ Session {session_num} recorded")
    
    # XP
    print("\\n⭐ EXPERIENCE POINTS:")
    xp_gained = input("XP gained this session (0 if none): ").strip()
    if xp_gained.isdigit():
        updates['xp_gained'] = int(xp_gained)
        print(f"✅ +{xp_gained} XP gained!")
        
        # Check for potential level up
        current_xp = int(xp_gained)  # Simplified - in real version would track total
        if current_xp >= 300:  # Rough estimate for level up potential
            print("🌟 You might be close to Level 3! (900 XP total needed)")
    
    # Current HP
    print("\\n💚 HIT POINTS:")
    current_hp = input("Current HP after session (or Enter to skip): ").strip()
    if current_hp.isdigit():
        updates['current_hp'] = int(current_hp)
        print(f"✅ Current HP: {current_hp}")
    
    # Equipment
    print("\\n🎒 NEW EQUIPMENT:")
    print("Enter new items (one per line, empty line when done):")
    new_equipment = []
    while True:
        item = input("Item: ").strip()
        if not item:
            break
        new_equipment.append(item)
        print(f"✅ Added: {item}")
    
    if new_equipment:
        updates['new_equipment'] = new_equipment
    
    # Currency changes
    print("\\n💰 CURRENCY CHANGES:")
    currency_changes = {}
    
    for coin_type, symbol in [('gp', '🥇'), ('sp', '🥈'), ('cp', '🥉')]:
        change = input(f"{symbol} {coin_type.upper()} gained/lost (+/-/0): ").strip()
        if change and (change.startswith('+') or change.startswith('-')) and change[1:].isdigit():
            currency_changes[coin_type] = int(change)
            print(f"✅ {change} {coin_type.upper()}")
        elif change == '0':
            print(f"➖ No {coin_type.upper()} change")
    
    if currency_changes:
        updates['currency_changes'] = currency_changes
    
    return updates

def save_character_data(char_data, filename="kazrek_epic_data.json"):
    """Save character data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(char_data, f, indent=2)
    print(f"💾 Character data saved to {filename}")

def generate_epic_summary(char_data, updates):
    """Generate epic session summary"""
    session_num = char_data.get('session', 'N/A')
    
    summary = f"""
🎨{'='*60}🎨
✨            KAZREK SPELLFORGE SESSION SUMMARY            ✨
🎨{'='*60}🎨

📅 SESSION {session_num}
📆 Date: {datetime.now().strftime('%A, %B %d, %Y')}
🧙‍♂️ Character: {char_data['name']} (Level {char_data['level']} {char_data['race']} {char_data['class']})

📊 SESSION RESULTS:
⭐ XP Gained: {updates.get('xp_gained', 0)}
🎒 New Equipment: {', '.join(updates.get('new_equipment', ['None']))}
💰 Currency: {', '.join([f"{v:+d} {k.upper()}" for k, v in updates.get('currency_changes', {}).items()])}

📈 CURRENT STATS:
💚 HP: {char_data.get('current_hp', '?')} / {char_data['hp_max']}
⭐ XP: {char_data.get('current_xp', '?')} / {char_data['next_level_xp']}
🥇 Gold: {char_data['currency'].get('gp', 0)} gp
🔮 Sorcery Points: {char_data.get('sorcery_points', 0)}

📁 FILES GENERATED:
📋 Kazrek_Epic_Sheet.html (Epic printable character sheet)
💾 kazrek_epic_data.json (Character data backup)
📝 epic_session_{session_num}_summary.txt (This summary)

🌟 NEXT SESSION PREP:
1. Open Kazrek_Epic_Sheet.html in browser
2. Enable "Background graphics" when printing
3. Print 3 pages for epic character sheets
4. Bring dice and prepare for adventure! 🎲

🐉 Ready for Epic Adventures! 🐉
"""
    
    filename = f"epic_session_{session_num}_summary.txt"
    with open(filename, 'w') as f:
        f.write(summary)
    
    print(summary)
    return filename

if __name__ == "__main__":
    try:
        # Epic welcome
        print("🎨✨🐉 KAZREK'S EPIC CHARACTER UPDATER 🐉✨🎨")
        print()
        
        # Get updates from user
        updates = interactive_update()
        
        if not updates:
            print("\\n➖ No updates provided. Generating fresh sheet anyway...")
            updates = {}
        
        # Update character data
        print("\\n🔄 Updating character data...")
        char_data = update_character_data(updates)
        
        # Save updated data
        save_character_data(char_data)
        
        # Generate new epic character sheet
        print("🎨 Generating EPIC character sheet...")
        generate_modern_sheet(char_data, "Kazrek_Epic_Sheet.html")
        
        # Generate session summary
        summary_file = generate_epic_summary(char_data, updates)
        
        print("\\n" + "🎨" + "="*60 + "🎨")
        print("✅               UPDATE COMPLETE!               ✅")
        print("🎨" + "="*60 + "🎨")
        print()
        print("📁 FILES READY:")
        print("  🎨 Kazrek_Epic_Sheet.html (Open in browser → Print with backgrounds)")
        print("  💾 kazrek_epic_data.json (Character data backup)")
        print(f"  📝 {summary_file} (Session recap)")
        print()
        print("🖨️  PRINT INSTRUCTIONS:")
        print("  1. Open Kazrek_Epic_Sheet.html in any browser")
        print("  2. File → Print (Ctrl/Cmd + P)")
        print("  3. Click 'More settings'")
        print("  4. ✅ Check 'Background graphics'")
        print("  5. Set margins to 'Minimum'")
        print("  6. Print 3 epic pages!")
        print()
        print("🐉 READY FOR EPIC ADVENTURES! 🐉")
        
    except KeyboardInterrupt:
        print("\\n\\n❌ Update cancelled. No worries, adventure awaits! 🗡️")
    except Exception as e:
        print(f"\\n💥 Epic error encountered: {e}")
        print("Fear not! Try again, brave adventurer! ⚔️")