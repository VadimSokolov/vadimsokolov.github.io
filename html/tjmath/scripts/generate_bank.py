#!/usr/bin/env python3
"""
Problem Bank Generator for TJ Math Packets
Generates 100 variant problems per focus area with worked solutions.
"""

import json
import re
import random
import math
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from fractions import Fraction

# Set seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

PACKETS_DIR = Path("/Users/vsokolov/www/html/tjmath/packets")
OUTPUT_FILE = Path("/Users/vsokolov/www/html/tjmath/bank.json")


def generate_problem_id(packet_num: int, section: str, variant_num: int) -> str:
    """Generate unique problem ID"""
    return f"P{packet_num}{section}{variant_num:03d}"


def parse_packet_file(filepath: Path) -> Dict[str, Any]:
    """Parse a packet file and extract metadata"""
    with open(filepath, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
        content = f.read()
    
    # Extract packet number and title from first line
    first_line = content.split('\n')[0].strip()
    match = re.match(r'Math Packet #(\d+)\s*[–\-—]\s*(.+)', first_line)  # Handle en-dash, hyphen, em-dash
    if match:
        packet_num = int(match.group(1))
        title = match.group(2).strip()
    else:
        packet_num = 0
        title = "Unknown"
    
    # Extract focus areas
    focus_pattern = r'Focus Areas\s*\n((?:\*.*\n)+)'
    focus_match = re.search(focus_pattern, content)
    focus_areas = []
    if focus_match:
        for line in focus_match.group(1).split('\n'):
            if line.strip().startswith('*'):
                focus_areas.append(line.strip()[1:].strip())
    
    # Extract sections
    sections = {}
    section_pattern = r'Section ([ABC]):\s*([^\n]+)'
    for match in re.finditer(section_pattern, content):
        section_letter = match.group(1)
        section_name = match.group(2).strip()
        sections[section_letter] = section_name
    
    return {
        'packet_num': packet_num,
        'title': title,
        'focus_areas': focus_areas,
        'sections': sections,
        'filepath': str(filepath)
    }


# ============================================================================
# PACKET 1: Distance, Work, Unit Conversion
# ============================================================================

def generate_packet1_sectionA(packet_num: int, section: str, count: int) -> List[Dict]:
    """Distance = Rate × Time"""
    problems = []
    templates = 10
    per_template = count // templates
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Simple distance
            speed = random.choice([40, 45, 50, 55, 60, 65, 70, 75, 80])
            time = random.choice([1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
            distance = speed * time
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A car travels at a constant speed of {speed} mph. How far does it travel in {time} hours?",
                "answer": f"{distance} miles",
                "solution": f"Formula: Distance = Speed × Time\nPlug in: Distance = {speed} mph × {time} hours = {distance} miles",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Find speed
            distance = random.choice([6, 8, 10, 12, 15, 18, 20, 24])
            time = random.choice([0.75, 1, 1.25, 1.5, 2, 2.5, 3])
            speed = distance / time
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A jogger runs {distance} miles in {time} hours. What is their average speed in mph?",
                "answer": f"{speed} mph",
                "solution": f"Formula: Speed = Distance ÷ Time\nSpeed = {distance} miles ÷ {time} hours = {speed} mph",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Find time
            speed = random.choice([10, 12, 15, 18, 20, 24, 25, 30])
            distance = random.choice([15, 18, 20, 24, 30, 36, 40, 45])
            time = distance / speed
            hours = int(time)
            minutes = int((time - hours) * 60)
            answer = f"{hours} hour{'s' if hours != 1 else ''}" + (f" {minutes} minutes" if minutes > 0 else "")
            solution = f"Formula: Time = Distance ÷ Speed\nTime = {distance} miles ÷ {speed} mph = {time} hours"
            if minutes > 0:
                solution += f"\n{time - hours} hours = {minutes} minutes"
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A cyclist rides at {speed} mph. How long will it take to travel {distance} miles?",
                "answer": answer,
                "solution": solution,
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Convert time and find speed
            distance = random.choice([100, 120, 135, 150, 180, 200])
            hours = random.choice([1, 2, 3])
            minutes = random.choice([15, 30, 45])
            total_hours = hours + minutes / 60
            speed = distance / total_hours
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A train travels {distance} miles in {hours} hours and {minutes} minutes. What is the average speed?",
                "answer": f"{speed:.2f} mph",
                "solution": f"Convert {minutes} minutes to hours: {minutes} ÷ 60 = {minutes/60} hours\nTotal time = {hours} + {minutes/60} = {total_hours} hours\nSpeed = {distance} miles ÷ {total_hours} hours = {speed:.2f} mph",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Meeting trains
            speed_a = random.choice([30, 35, 40, 45, 50])
            speed_b = random.choice([50, 55, 60, 65, 70])
            distance = random.choice([200, 240, 270, 300, 350, 400])
            time = distance / (speed_a + speed_b)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Train A leaves City X traveling east at {speed_a} mph. Train B leaves City Y, {distance} miles away, traveling west at {speed_b} mph. When do they meet?",
                "answer": f"{time:.2f} hours",
                "solution": f"Let time = t hours. Train A goes {speed_a}t miles. Train B goes {speed_b}t miles.\nTotal distance = {distance} miles → {speed_a}t + {speed_b}t = {distance}\n{speed_a + speed_b}t = {distance} → t = {time:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Upstream/downstream
            downstream = random.choice([10, 12, 14, 15, 16])
            upstream = random.choice([6, 7, 8, 9, 10])
            distance = random.choice([30, 35, 40, 45, 50])
            time_down = distance / downstream
            time_up = distance / upstream
            total = time_down + time_up
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A boat travels downstream at {downstream} mph and upstream at {upstream} mph. If the river is {distance} miles long, how long does a round trip take?",
                "answer": f"{total:.2f} hours",
                "solution": f"Time downstream = {distance} ÷ {downstream} = {time_down:.2f} hours\nTime upstream = {distance} ÷ {upstream} = {time_up:.2f} hours\nTotal time = {time_down:.2f} + {time_up:.2f} = {total:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Average speed two parts
            total_dist = random.choice([100, 120, 140, 160, 180, 200])
            half = total_dist / 2
            speed1 = random.choice([40, 45, 50, 55, 60])
            speed2 = random.choice([60, 65, 70, 75, 80])
            time1 = half / speed1
            time2 = half / speed2
            total_time = time1 + time2
            avg = total_dist / total_time
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A car drives half of a {total_dist}-mile trip at {speed1} mph and the other half at {speed2} mph. What is the average speed?",
                "answer": f"{avg:.1f} mph",
                "solution": f"First half: {half} ÷ {speed1} = {time1:.2f} hours\nSecond half: {half} ÷ {speed2} = {time2:.2f} hours\nTotal time = {total_time:.2f} hours\nAverage speed = {total_dist} ÷ {total_time:.2f} = {avg:.1f} mph",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Meeting runners
            distance = random.choice([8, 10, 12, 15, 18, 20])
            speed1 = random.choice([4, 5, 6, 7])
            speed2 = random.choice([3, 4, 5, 6])
            time = distance / (speed1 + speed2)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Two runners start {distance} miles apart and run toward each other. One runs at {speed1} mph and the other at {speed2} mph. When do they meet?",
                "answer": f"{time:.2f} hours",
                "solution": f"Combined speed = {speed1} + {speed2} = {speed1 + speed2} mph\nTime = {distance} ÷ {speed1 + speed2} = {time:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Uphill/downhill
            uphill = random.choice([2, 2.5, 3, 3.5])
            downhill = random.choice([4, 4.5, 5, 5.5, 6])
            total_time = random.choice([3, 4, 5, 6])
            distance = total_time / (1/uphill + 1/downhill)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A hiker walks uphill at {uphill} mph and downhill at {downhill} mph. If the round trip takes {total_time} hours, how long is the trail one way?",
                "answer": f"{distance:.2f} miles",
                "solution": f"Let distance = d miles\nTime up = d/{uphill}, time down = d/{downhill}\nTotal: d/{uphill} + d/{downhill} = {total_time}\nd = {total_time} ÷ {1/uphill + 1/downhill:.3f} = {distance:.2f} miles",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Wind round trip
            distance = random.choice([300, 350, 400, 450, 500])
            airspeed = random.choice([120, 140, 150, 160, 180])
            wind = random.choice([20, 25, 30, 35, 40])
            time_with = distance / (airspeed + wind)
            time_against = distance / (airspeed - wind)
            total = time_with + time_against
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A plane travels {distance} miles with a {wind} mph tailwind and returns against a {wind} mph headwind. If its airspeed is {airspeed} mph, how long is the round trip?",
                "answer": f"{total:.2f} hours",
                "solution": f"With wind: {airspeed + wind} mph → Time = {distance} ÷ {airspeed + wind} = {time_with:.2f} hours\nAgainst wind: {airspeed - wind} mph → Time = {distance} ÷ {airspeed - wind} = {time_against:.2f} hours\nTotal = {total:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


def generate_packet1_sectionB(packet_num: int, section: str, count: int) -> List[Dict]:
    """Work and Rate problems"""
    problems = []
    templates = 10
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Fraction per hour
            hours = random.choice([3, 4, 5, 6, 7, 8, 10, 12])
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A machine completes a job in {hours} hours. What fraction of the job does it complete in 1 hour?",
                "answer": f"1/{hours} of the job per hour",
                "solution": f"It takes {hours} hours to do 1 job, so in 1 hour, it finishes 1/{hours} of the job.",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Two machines together
            time_a = random.choice([3, 4, 5, 6, 8])
            time_b = random.choice([4, 5, 6, 8, 10, 12])
            rate_a = Fraction(1, time_a)
            rate_b = Fraction(1, time_b)
            combined = rate_a + rate_b
            time_together = 1 / combined
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"If two machines work together, one finishing the job in {time_a} hours and the other in {time_b} hours, how long will they take together?",
                "answer": f"{float(time_together):.2f} hours",
                "solution": f"Machine A rate = 1/{time_a}, Machine B rate = 1/{time_b}\nTogether: 1/{time_a} + 1/{time_b} = {float(combined):.4f} job/hour\nTime = 1 ÷ {float(combined):.4f} = {float(time_together):.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Two faucets, one stops
            time_a = random.choice([2, 3, 4, 5])
            time_b = random.choice([3, 4, 5, 6])
            rate_a = Fraction(1, time_a)
            rate_b = Fraction(1, time_b)
            work_done = float((rate_a + rate_b) * 1)
            remaining = 1 - work_done
            time_remaining = remaining / float(rate_a)
            total = 1 + time_remaining
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A faucet fills a tank in {time_a} hours. A second faucet fills it in {time_b} hours. If both are turned on, but the second faucet is turned off after 1 hour, how long in total to fill?",
                "answer": f"{total:.2f} hours",
                "solution": f"Faucet A = 1/{time_a}, B = 1/{time_b}\nCombined for 1 hour = {work_done:.4f}\nRemaining = {remaining:.4f}\nA finishes: {remaining:.4f} ÷ (1/{time_a}) = {time_remaining:.2f} hours\nTotal = {total:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Workers, one leaves
            time_a = random.choice([8, 10, 12, 15])
            time_b = random.choice([6, 8, 10, 12])
            work_together = random.choice([2, 3, 4])
            rate_a = Fraction(1, time_a)
            rate_b = Fraction(1, time_b)
            work_done = float((rate_a + rate_b) * work_together)
            remaining = 1 - work_done
            time_remaining = remaining / float(rate_a)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Worker A completes a task in {time_a} hours. Worker B takes {time_b} hours. They work together for {work_together} hours, then B leaves. How long does A need to finish the rest?",
                "answer": f"{time_remaining:.2f} hours",
                "solution": f"A = 1/{time_a}, B = 1/{time_b}\nTogether: {float(rate_a + rate_b):.4f} job/hour\n{work_together} hours × {float(rate_a + rate_b):.4f} = {work_done:.4f}\nRemaining: {remaining:.4f} ÷ (1/{time_a}) = {time_remaining:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Robots cleaning rooms
            robots1 = random.choice([3, 4, 5])
            rooms1 = random.choice([9, 12, 15, 18])
            hours1 = random.choice([3, 4, 6])
            robots2 = random.choice([4, 5, 6, 8])
            rooms2 = random.choice([12, 15, 18, 20, 24])
            rate_per_robot = rooms1 / (robots1 * hours1)
            time2 = rooms2 / (robots2 * rate_per_robot)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"{robots1} robots can clean {rooms1} rooms in {hours1} hours. How long will {robots2} robots take to clean {rooms2} rooms?",
                "answer": f"{time2:.2f} hours",
                "solution": f"Rate = {rooms1} ÷ {hours1} = {rooms1/hours1:.2f} rooms/hour (all {robots1} robots)\n1 robot = {rate_per_robot:.2f} rooms/hr\n{robots2} robots = {robots2 * rate_per_robot:.2f} rooms/hr\nTime = {rooms2} ÷ {robots2 * rate_per_robot:.2f} = {time2:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Printer pages
            rate = random.choice([4, 5, 6, 8, 10])
            pages = random.choice([200, 240, 300, 360, 400, 480])
            time = pages / rate
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A printer prints {rate} pages per minute. How many minutes to print {pages} pages?",
                "answer": f"{time:.0f} minutes",
                "solution": f"{pages} ÷ {rate} = {time:.0f} minutes",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Mowing together
            time_a = random.choice([30, 40, 45, 50, 60])
            time_b = random.choice([40, 50, 60, 70, 80])
            rate_a = Fraction(1, time_a)
            rate_b = Fraction(1, time_b)
            combined = rate_a + rate_b
            time_together = 1 / combined
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Alice mows a lawn in {time_a} minutes. Bob does the same in {time_b} minutes. How long if they mow together?",
                "answer": f"{float(time_together):.2f} minutes",
                "solution": f"A = 1/{time_a}, B = 1/{time_b}\nTogether: {float(combined):.6f}\nTime = 1 ÷ {float(combined):.6f} = {float(time_together):.2f} minutes",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Pumps emptying pool
            pumps1 = random.choice([2, 3, 4])
            time1 = random.choice([2, 3, 4])
            pumps2 = random.choice([2, 3])
            rate_per_pump = 1 / (pumps1 * time1)
            time2 = 1 / (pumps2 * rate_per_pump)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"{pumps1} pumps can empty a pool in {time1} hours. If only {pumps2} pumps are working, how long will it take?",
                "answer": f"{time2:.2f} hours",
                "solution": f"{pumps1} pumps = 1/{time1} job/hr → 1 pump = 1/{pumps1 * time1}\n{pumps2} pumps = {pumps2}/{pumps1 * time1} job/hr\nTime = {time2:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Editor with breaks
            rate = random.choice([15, 18, 20, 24, 25])
            pages = random.choice([100, 120, 150, 180, 200])
            breaks = random.choice([2, 3, 4])
            break_len = random.choice([10, 15, 20])
            work_time = pages / rate
            total = work_time + (breaks * break_len / 60)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"An editor proofreads {rate} pages/hr. A report is {pages} pages. If they take {breaks} {break_len}-minute breaks, how long to finish?",
                "answer": f"{total:.2f} hours",
                "solution": f"Work time = {pages} ÷ {rate} = {work_time:.2f} hours\nBreak time = {breaks * break_len / 60:.2f} hours\nTotal = {total:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Partial work rate
            numerator = random.choice([1, 2, 3])
            denominator = random.choice([2, 3, 4, 5])
            if numerator >= denominator:
                numerator = denominator - 1
            fraction = Fraction(numerator, denominator)
            time_taken = random.choice([1, 1.5, 2, 2.5, 3])
            total_time = time_taken / float(fraction)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Jack paints {numerator}/{denominator} of a wall in {time_taken} hours. At the same rate, how long to paint the entire wall?",
                "answer": f"{total_time:.2f} hours",
                "solution": f"{time_taken} ÷ ({numerator}/{denominator}) = {total_time:.2f} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


def generate_packet1_sectionC(packet_num: int, section: str, count: int) -> List[Dict]:
    """Unit Conversions"""
    problems = []
    templates = 8
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Hours to minutes/seconds
            hours = random.choice([2.5, 3, 3.5, 4, 4.5, 5])
            minutes = hours * 60
            seconds = minutes * 60
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Convert {hours} hours to minutes and seconds.",
                "answer": f"{int(minutes)} minutes and {int(seconds)} seconds",
                "solution": f"1 hour = 60 minutes → {hours} hours = {int(minutes)} minutes\n1 minute = 60 seconds → {int(minutes)} × 60 = {int(seconds)} seconds",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Liters to milliliters
            liters = random.choice([1.5, 2, 2.5, 3, 3.5, 4, 5])
            ml = liters * 1000
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A recipe calls for {liters} liters of water. How many milliliters is this?",
                "answer": f"{int(ml)} milliliters",
                "solution": f"1 liter = 1000 milliliters\n{liters} liters = {int(ml)} milliliters",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # km/h to mph
            kmh = random.choice([80, 90, 100, 110, 120])
            mph = kmh / 1.61
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A car travels at {kmh} kilometers per hour. What is this speed in miles per hour? (1 mi = 1.61 km)",
                "answer": f"{mph:.1f} mph",
                "solution": f"1 km ≈ 0.6211 miles\n{kmh} km ≈ {mph:.1f} mph",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Fuel consumption
            rate = random.choice([800, 900, 1000, 1100, 1200])
            hours = random.choice([2, 3])
            minutes = random.choice([15, 30, 45])
            total_hours = hours + minutes / 60
            fuel = rate * total_hours
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A plane consumes {rate} lbs of fuel per hour. How many pounds does it burn in {hours} hours and {minutes} minutes?",
                "answer": f"{fuel:.0f} lbs",
                "solution": f"{minutes} minutes = {minutes/60} hours\nTotal = {total_hours} hours\nFuel = {rate} × {total_hours} = {fuel:.0f} lbs",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Gallons to liters per second
            gpm = random.choice([3, 4, 5, 6, 8])
            lpm = gpm * 3.785
            lps = lpm / 60
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Convert {gpm} gallons per minute to liters per second. (1 gal = 3.785 L)",
                "answer": f"{lps:.3f} L/sec",
                "solution": f"{gpm} gal/min = {lpm:.3f} L/min\n{lpm:.3f} ÷ 60 = {lps:.3f} L/sec",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Pool fill time
            diameter = random.choice([8, 10, 12, 14])
            depth = random.choice([2, 3, 4])
            rate = random.choice([1, 1.5, 2, 2.5])
            radius = diameter / 2
            volume = math.pi * radius * radius * depth
            time = volume / rate
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A circular pool with diameter {diameter} ft and depth {depth} ft is filled at {rate} cubic ft/min. How long to fill it?",
                "answer": f"{time:.0f} minutes",
                "solution": f"Radius = {radius} ft\nVolume = π × {radius}² × {depth} = {volume:.2f} ft³\nTime = {volume:.2f} ÷ {rate} = {time:.0f} minutes",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # mg to grams/kg
            mg = random.choice([2000, 3000, 4000, 5000, 6000, 8000])
            grams = mg / 1000
            kg = grams / 1000
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Convert {mg} mg to grams and kilograms.",
                "answer": f"{grams} grams and {kg} kg",
                "solution": f"1000 mg = 1 g → {mg} mg = {grams} grams\n1000 g = 1 kg → {grams} g = {kg} kg",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        else:  # Distance and average speed
            speed1 = random.choice([50, 55, 60, 65])
            time1 = random.choice([2, 3])
            speed2 = random.choice([35, 40, 45])
            time2 = random.choice([2, 3, 4])
            dist1 = speed1 * time1
            dist2 = speed2 * time2
            total_dist = dist1 + dist2
            total_time = time1 + time2
            avg = total_dist / total_time
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A truck moves at {speed1} mph for {time1} hours, then {speed2} mph for {time2} hours. What's the total distance and average speed?",
                "answer": f"{total_dist} miles, {avg:.1f} mph",
                "solution": f"First: {speed1} × {time1} = {dist1} miles\nSecond: {speed2} × {time2} = {dist2} miles\nTotal distance = {total_dist} miles\nAverage speed = {total_dist} ÷ {total_time} = {avg:.1f} mph",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
    
    return problems


# ============================================================================
# PACKET 2: Ratios, Linear Equations, Area/Volume
# ============================================================================

def generate_packet2_sectionA(packet_num: int, section: str, count: int) -> List[Dict]:
    """Ratios, Proportions, Percents"""
    problems = []
    templates = 10
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Ratio mixture
            r1, r2, r3 = random.choice([(2,3,5), (1,2,3), (3,4,5), (2,5,3)])
            total_vol = random.choice([40, 50, 60, 80, 100])
            parts = r1 + r2 + r3
            per_part = total_vol / parts
            blue = r2 * per_part
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A mixture contains red, blue, and yellow paint in a {r1}:{r2}:{r3} ratio. If the total volume is {total_vol} liters, how many liters of blue paint are there?",
                "answer": f"{blue} liters",
                "solution": f"Total parts = {r1} + {r2} + {r3} = {parts}\nEach part = {total_vol} ÷ {parts} = {per_part} liters\nBlue = {r2} × {per_part} = {blue} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Metal alloy ratio
            r1, r2 = random.choice([(7,3), (3,2), (4,1), (5,2)])
            total = random.choice([60, 70, 80, 90, 100])
            parts = r1 + r2
            per_part = total / parts
            zinc = r2 * per_part
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A metal alloy is made by combining copper and zinc in a {r1}:{r2} ratio. If you want {total} grams of alloy, how much zinc do you need?",
                "answer": f"{zinc} grams",
                "solution": f"Total parts = {parts}\nEach part = {total} ÷ {parts} = {per_part} grams\nZinc = {r2} × {per_part} = {zinc} grams",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Ratio change with addition
            r1, r2 = random.choice([(5,4), (3,2), (4,3)])
            added = random.choice([10, 12, 15, 18])
            # r1*x / (r2*x + added) = 1
            x = added / (r1 - r2)
            girls = r1 * x
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"The ratio of girls to boys at a camp is {r1}:{r2}. After {added} more boys join, the ratio becomes {r1}:{r1}. How many girls are there?",
                "answer": f"{girls:.0f} girls",
                "solution": f"Let girls = {r1}x, boys = {r2}x\nAfter: {r1}x = {r2}x + {added}\n{r1-r2}x = {added} → x = {x:.0f}\nGirls = {r1} × {x:.0f} = {girls:.0f}",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Proportion distance
            dist1 = random.choice([120, 150, 180, 200])
            gal1 = random.choice([4, 5, 6])
            gal2 = random.choice([10, 12, 13, 15])
            rate = dist1 / gal1
            dist2 = rate * gal2
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A car travels {dist1} miles on {gal1} gallons of fuel. At the same rate, how far can it travel on {gal2} gallons?",
                "answer": f"{dist2:.0f} miles",
                "solution": f"Rate = {dist1} ÷ {gal1} = {rate} miles per gallon\nDistance = {rate} × {gal2} = {dist2:.0f} miles",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Percent correct/wrong
            total = random.choice([60, 80, 100])
            percent = random.choice([70, 75, 80, 85])
            correct = total * percent / 100
            wrong = total - correct
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A student answered {percent}% of the {total} questions correctly on a test. How many were incorrect?",
                "answer": f"{wrong:.0f} questions",
                "solution": f"Correct = {percent}% of {total} = {correct:.0f}\nWrong = {total} - {correct:.0f} = {wrong:.0f}",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Sequential discounts
            original = random.choice([80, 100, 120, 150])
            disc1 = random.choice([20, 25, 30])
            disc2 = random.choice([10, 15])
            after1 = original * (1 - disc1/100)
            final = after1 * (1 - disc2/100)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A store has a {disc1}% off sale, followed by an additional {disc2}% off the discounted price. If an item was originally ${original}, what's the final price?",
                "answer": f"${final:.2f}",
                "solution": f"First discount: ${original} × {1-disc1/100} = ${after1:.2f}\nSecond discount: ${after1:.2f} × {1-disc2/100} = ${final:.2f}",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Discount then tax
            original = random.choice([800, 1000, 1200, 1500])
            discount = random.choice([10, 15, 20])
            tax = random.choice([6, 7, 8, 9])
            after_disc = original * (1 - discount/100)
            final = after_disc * (1 + tax/100)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A computer originally priced at ${original} is discounted by {discount}%. After tax of {tax}%, what's the total price?",
                "answer": f"${final:.2f}",
                "solution": f"After discount: ${original} × {1-discount/100} = ${after_disc:.2f}\nAfter tax: ${after_disc:.2f} × {1+tax/100} = ${final:.2f}",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Population growth
            initial = random.choice([400000, 450000, 500000])
            final = initial + random.choice([100000, 120000, 150000])
            percent = ((final - initial) / initial) * 100
            annual = percent / 2
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A city's population grows from {initial} to {final} in 2 years. What is the approximate annual percent growth rate (assuming constant yearly growth)?",
                "answer": f"{annual:.1f}% per year",
                "solution": f"Total increase = {final - initial}\nPercent = {percent:.1f}%\nAnnual ≈ {annual:.1f}% per year",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Leakage percent
            initial = random.choice([200, 250, 300])
            percent_lost = random.choice([10, 12, 15, 18])
            remaining = initial * (1 - percent_lost/100)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A water tank loses {percent_lost}% of its water due to leakage. If it initially had {initial} liters, how much water is left?",
                "answer": f"{remaining:.0f} liters",
                "solution": f"Water left = {100-percent_lost}% = {initial} × {1-percent_lost/100} = {remaining:.0f} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Study time ratio
            r1, r2, r3 = random.choice([(2,3,4), (1,2,3), (3,4,5)])
            total_hours = random.choice([9, 12, 15, 18])
            parts = r1 + r2 + r3
            per_part = total_hours / parts
            second = r2 * per_part
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A student splits {total_hours} study hours among 3 subjects in a {r1}:{r2}:{r3} ratio. How many hours are spent on the second subject?",
                "answer": f"{second} hours",
                "solution": f"Total parts = {parts}\nEach part = {total_hours} ÷ {parts} = {per_part} hours\nSecond subject = {r2} × {per_part} = {second} hours",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


def generate_packet2_sectionB(packet_num: int, section: str, count: int) -> List[Dict]:
    """Linear Equations & Word Problems"""
    problems = []
    templates = 10
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Solve linear equation
            a = random.choice([2, 3, 4])
            b = random.choice([3, 4, 5])
            c = random.choice([3, 4, 5, 6])
            d = random.choice([1, 2, 3])
            # a(bx - c) = d(x + 1) + 2
            # abx - ac = dx + d + 2
            # abx - dx = ac + d + 2
            # x(ab - d) = ac + d + 2
            x = (a*c + d + 2) / (a*b - d)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Solve: {a}({b}x - {c}) = {d}(x + 1) + 2",
                "answer": f"x = {x:.1f}",
                "solution": f"Expand: {a*b}x - {a*c} = {d}x + {d} + 2\n{a*b}x - {d}x = {a*c + d + 2}\n{a*b - d}x = {a*c + d + 2}\nx = {x:.1f}",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Fraction equation
            a, b = random.choice([(2,3), (3,4), (3,5)])
            c, d = random.choice([(1,2), (2,3), (1,3)])
            # (ax - b)/c = (x + d)/e
            e = random.choice([2, 3])
            # e(ax - b) = c(x + d)
            # eax - eb = cx + cd
            # x(ea - c) = eb + cd
            x = (e*b + c*d) / (e*a - c)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Solve for x: ({a}x - {b})/{c} = (x + {d})/{e}",
                "answer": f"x = {x:.1f}",
                "solution": f"Cross multiply: {e}({a}x - {b}) = {c}(x + {d})\n{e*a}x - {e*b} = {c}x + {c*d}\nx = {x:.1f}",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Markers and notebooks
            markers = random.choice([5, 6, 7, 8])
            notebooks = random.choice([2, 3, 4])
            notebook_cost = random.choice([3, 4, 5])
            total = random.choice([35, 40, 45, 50])
            marker_cost = (total - notebooks * notebook_cost) / markers
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"If {markers} markers and {notebooks} notebooks cost ${total}, and each notebook costs ${notebook_cost}, what is the cost of one marker?",
                "answer": f"${marker_cost:.2f}",
                "solution": f"Notebook total: {notebooks} × ${notebook_cost} = ${notebooks * notebook_cost}\nMarkers: ${total} - ${notebooks * notebook_cost} = ${total - notebooks * notebook_cost}\nEach marker: ${total - notebooks * notebook_cost} ÷ {markers} = ${marker_cost:.2f}",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Subscription cost
            fixed = random.choice([4, 5, 6, 8])
            daily = random.choice([1, 1.5, 2, 2.5])
            total = random.choice([15, 18, 20, 25])
            days = (total - fixed) / daily
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A subscription costs a fixed fee of ${fixed} plus ${daily} per day. If a student pays ${total} in total, how many days did they subscribe?",
                "answer": f"{days:.0f} days",
                "solution": f"${fixed} + ${daily}d = ${total}\n${daily}d = ${total - fixed}\nd = {days:.0f} days",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Supplementary angles
            extra = random.choice([15, 20, 25, 30])
            # x + (2x + extra) = 180
            # 3x = 180 - extra
            x = (180 - extra) / 3
            other = 2*x + extra
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Two angles are supplementary. One is {extra}° more than twice the other. What are the angles?",
                "answer": f"{x:.1f}° and {other:.1f}°",
                "solution": f"Let one = x, other = 2x + {extra}\nx + 2x + {extra} = 180\n3x = {180 - extra}\nx = {x:.1f}°, other = {other:.1f}°",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Age problem
            years_future = random.choice([4, 5, 6])
            total_future = random.choice([40, 45, 50, 55])
            multiplier = random.choice([2, 3])
            extra = random.choice([2, 3, 4, 5])
            # Alice = x, John = mx + extra
            # In years_future: (x + years_future) + (mx + extra + years_future) = total_future
            # x + mx = total_future - 2*years_future - extra
            x = (total_future - 2*years_future - extra) / (1 + multiplier)
            john = multiplier * x + extra
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"John's age is {extra} years more than {multiplier} times Alice's age. In {years_future} years, their total age will be {total_future}. How old is each now?",
                "answer": f"Alice = {x:.1f}, John = {john:.1f}",
                "solution": f"Alice = x, John = {multiplier}x + {extra}\nIn {years_future} years: (x + {years_future}) + ({multiplier}x + {extra} + {years_future}) = {total_future}\n{1+multiplier}x = {total_future - 2*years_future - extra}\nAlice = {x:.1f}, John = {john:.1f}",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Increase then decrease
            inc_pct = random.choice([30, 40, 50])
            dec_pct = random.choice([20, 25, 30])
            result = random.choice([70, 80, 84, 90])
            multiplier = (1 + inc_pct/100) * (1 - dec_pct/100)
            original = result / multiplier
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A number is increased by {inc_pct}%, then decreased by {dec_pct}%. If the result is {result}, what was the original number?",
                "answer": f"{original:.1f}",
                "solution": f"Total multiplier = {1+inc_pct/100} × {1-dec_pct/100} = {multiplier:.3f}\nx × {multiplier:.3f} = {result}\nx = {original:.1f}",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Girls and boys
            extra = random.choice([2, 3, 4, 5])
            total = random.choice([25, 30, 33, 35, 40])
            # girls = 2*boys + extra
            # boys + girls = total
            # boys + 2*boys + extra = total
            boys = (total - extra) / 3
            girls = 2*boys + extra
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A class has {extra} more girls than twice the number of boys. There are {total} students total. How many girls?",
                "answer": f"{girls:.0f} girls",
                "solution": f"Let boys = x, girls = 2x + {extra}\nx + 2x + {extra} = {total}\n3x = {total - extra}\nx = {boys:.0f}, girls = {girls:.0f}",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Rope ratio
            r1, r2, r3 = random.choice([(2,3,5), (1,2,4), (2,4,6)])
            total_len = random.choice([40, 50, 60, 70])
            parts = r1 + r2 + r3
            longest = (r3 / parts) * total_len
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A {total_len}-foot rope is cut into 3 pieces in a {r1}:{r2}:{r3} ratio. How long is the longest piece?",
                "answer": f"{longest:.1f} feet",
                "solution": f"Total parts = {parts}\nEach part = {total_len} ÷ {parts} = {total_len/parts:.2f} feet\nLongest = {r3} × {total_len/parts:.2f} = {longest:.1f} feet",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Rectangle dimensions
            multiplier = random.choice([2, 3, 4])
            area = random.choice([48, 60, 72, 96, 108])
            # length = m * width
            # width * m * width = area
            # width^2 = area / m
            width = math.sqrt(area / multiplier)
            length = multiplier * width
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A rectangular garden is {multiplier} times as long as it is wide. If the area is {area} m², what are its dimensions?",
                "answer": f"{width:.0f} m by {length:.0f} m",
                "solution": f"Let width = w, length = {multiplier}w\nArea = w × {multiplier}w = {multiplier}w² = {area}\nw² = {area/multiplier}\nw = {width:.0f} m, length = {length:.0f} m",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


def generate_packet2_sectionC(packet_num: int, section: str, count: int) -> List[Dict]:
    """Area, Volume, and Geometry"""
    problems = []
    templates = 10
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Heron's formula
            sides = random.choice([(13,14,15), (5,12,13), (7,8,9), (10,11,12)])
            a, b, c = sides
            s = (a + b + c) / 2
            area = math.sqrt(s * (s-a) * (s-b) * (s-c))
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A triangle has sides {a} cm, {b} cm, and {c} cm. Use Heron's formula to find the area.",
                "answer": f"{area:.2f} cm²",
                "solution": f"Semi-perimeter s = ({a} + {b} + {c})/2 = {s}\nArea = √[s(s-a)(s-b)(s-c)] = √[{s}×{s-a}×{s-b}×{s-c}] = {area:.2f} cm²",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Circle area to radius
            area = random.choice([78.5, 113, 154, 201, 254])
            radius = math.sqrt(area / 3.14)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A circular garden has an area of {area} m². Find the radius. (Use π ≈ 3.14)",
                "answer": f"{radius:.1f} m",
                "solution": f"Area = π × r²\n{area} = 3.14 × r²\nr² = {area/3.14:.2f}\nr = {radius:.1f} m",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Box surface area
            l, w = random.choice([(3,2), (4,3), (5,2), (4,2)])
            sa = random.choice([70, 80, 94, 100, 110])
            # SA = 2(lw + lh + wh)
            # sa = 2(lw + h(l+w))
            # h = (sa/2 - lw) / (l+w)
            h = (sa/2 - l*w) / (l + w)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A rectangular box has a surface area of {sa} cm² and dimensions {l} cm × {w} cm × h. What is h?",
                "answer": f"{h:.1f} cm",
                "solution": f"SA = 2(lw + lh + wh)\n{sa} = 2({l*w} + {l}h + {w}h)\n{sa/2} = {l*w} + {l+w}h\nh = {h:.1f} cm",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Cube surface area
            sa = random.choice([96, 150, 216, 294])
            edge = math.sqrt(sa / 6)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A cube has surface area {sa} cm². What is its edge length?",
                "answer": f"{edge:.0f} cm",
                "solution": f"SA = 6a²\n{sa} = 6a²\na² = {sa/6:.0f}\na = {edge:.0f} cm",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Cylinder volume to radius
            volume = random.choice([157, 314, 471, 628])
            height = random.choice([4, 5, 6, 8])
            # V = πr²h
            radius = math.sqrt(volume / (3.14 * height))
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A cylinder has volume {volume} cm³ and height {height} cm. Find its radius. (Use π ≈ 3.14)",
                "answer": f"{radius:.2f} cm",
                "solution": f"V = π × r² × h\n{volume} = 3.14 × r² × {height}\nr² = {volume/(3.14*height):.2f}\nr = {radius:.2f} cm",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Cone volume to radius
            volume = random.choice([209, 314, 419, 523])
            height = random.choice([8, 10, 12, 15])
            # V = (1/3)πr²h
            radius = math.sqrt(volume / (3.14 * height / 3))
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A cone has height {height} cm and volume {volume} cm³. What is the radius? (Use π ≈ 3.14)",
                "answer": f"{radius:.2f} cm",
                "solution": f"V = (1/3) × π × r² × h\n{volume} = (1/3) × 3.14 × r² × {height}\nr² = {volume/(3.14*height/3):.2f}\nr = {radius:.2f} cm",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Circular track laps
            diameter = random.choice([50, 60, 70, 80, 100])
            laps = random.choice([3, 4, 5, 6])
            circumference = 3.14 * diameter
            distance = circumference * laps
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A circular track has a diameter of {diameter} m. A runner completes {laps} full laps. How far did they run?",
                "answer": f"{distance:.1f} m",
                "solution": f"Circumference = π × d = 3.14 × {diameter} = {circumference:.1f} m\nTotal = {circumference:.1f} × {laps} = {distance:.1f} m",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Pythagorean triple
            triples = [(3,4,5), (5,12,13), (8,15,17), (7,24,25), (9,40,41)]
            a, b, c = random.choice(triples)
            area = (a * b) / 2
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A triangle has sides {a} cm, {b} cm, and {c} cm. Prove it's a right triangle and find the area.",
                "answer": f"{area:.0f} cm²",
                "solution": f"Check: {a}² + {b}² = {a**2} + {b**2} = {a**2 + b**2} = {c}² = {c**2}\nIt's a right triangle.\nArea = (1/2) × {a} × {b} = {area:.0f} cm²",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Square and circle same perimeter
            side = random.choice([6, 8, 10, 12])
            perimeter = 4 * side
            radius = perimeter / (2 * 3.14)
            area = 3.14 * radius * radius
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A square and a circle have the same perimeter. The square has side length {side} cm. What is the area of the circle? (Use π ≈ 3.14)",
                "answer": f"{area:.2f} cm²",
                "solution": f"Square perimeter = 4 × {side} = {perimeter} cm\nCircle: 2πr = {perimeter} → r = {radius:.2f} cm\nArea = π × r² = 3.14 × {radius:.2f}² = {area:.2f} cm²",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Trapezoid and triangle same area
            base1, base2 = random.choice([(8,16), (10,20), (12,18), (10,16)])
            height1 = random.choice([5, 6, 8])
            trap_area = (base1 + base2) * height1 / 2
            tri_base = random.choice([12, 15, 18, 20])
            tri_height = 2 * trap_area / tri_base
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A trapezoid has bases {base1} cm and {base2} cm and height {height1} cm. A triangle has the same area. What is the height of that triangle if its base is {tri_base} cm?",
                "answer": f"{tri_height:.1f} cm",
                "solution": f"Trapezoid area = (1/2)({base1} + {base2}) × {height1} = {trap_area:.0f} cm²\nTriangle: {trap_area:.0f} = (1/2) × {tri_base} × h\nh = {tri_height:.1f} cm",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


# ============================================================================
# PACKET 3: Mixtures, Density, and Sequences
# ============================================================================

def generate_packet3_sectionA(packet_num: int, section: str, count: int) -> List[Dict]:
    """Mixture Problems"""
    problems = []
    templates = 10
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Add pure substance to increase concentration
            initial_vol = random.choice([8, 10, 12, 15, 20])
            initial_pct = random.choice([20, 25, 30, 35, 40])
            target_pct = random.choice([45, 50, 55, 60])
            # initial_vol * initial_pct + x = (initial_vol + x) * target_pct
            x = (initial_vol * initial_pct - initial_vol * target_pct) / (target_pct - 100)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A {initial_vol}-liter solution is {initial_pct}% acid. How many liters of pure acid must be added to make it a {target_pct}% acid solution?",
                "answer": f"{x:.2f} liters",
                "solution": f"Initial acid: {initial_vol} × {initial_pct/100} = {initial_vol * initial_pct/100} L\nLet x = liters added\n({initial_vol * initial_pct/100} + x) / ({initial_vol} + x) = {target_pct/100}\nSolving: x = {x:.2f} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Add water to dilute
            initial_vol = random.choice([4, 5, 6, 8])
            initial_pct = random.choice([40, 50, 60])
            target_pct = random.choice([20, 25, 30])
            x = initial_vol * (initial_pct - target_pct) / target_pct
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"How many liters of water should be added to {initial_vol} liters of a {initial_pct}% salt solution to reduce it to a {target_pct}% salt solution?",
                "answer": f"{x:.2f} liters",
                "solution": f"Salt: {initial_vol} × {initial_pct/100} = {initial_vol * initial_pct/100} L\n{initial_vol * initial_pct/100} / ({initial_vol} + x) = {target_pct/100}\nx = {x:.2f} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Drain and replace
            vol = random.choice([15, 20, 25])
            initial_pct = random.choice([25, 30, 35])
            target_pct = random.choice([10, 12, 15])
            x = vol * (initial_pct - target_pct) / initial_pct
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A tank contains {vol} liters of a {initial_pct}% sugar solution. How much of the solution must be drained and replaced with pure water to get a {target_pct}% sugar solution?",
                "answer": f"{x:.2f} liters",
                "solution": f"Sugar: {vol} × {initial_pct/100} = {vol * initial_pct/100} L\nDraining x removes {initial_pct/100}x sugar\n({vol * initial_pct/100} - {initial_pct/100}x) / {vol} = {target_pct/100}\nx = {x:.2f} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Mix two solutions
            vol1 = random.choice([3, 4, 5])
            pct1 = random.choice([10, 15, 20])
            vol2 = random.choice([5, 6, 7])
            pct2 = random.choice([25, 30, 35])
            result_pct = (vol1 * pct1 + vol2 * pct2) / (vol1 + vol2)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"You mix {vol1} liters of a {pct1}% acid solution with {vol2} liters of a {pct2}% acid solution. What is the concentration of the resulting mixture?",
                "answer": f"{result_pct:.1f}%",
                "solution": f"Acid from first: {vol1} × {pct1/100} = {vol1 * pct1/100} L\nAcid from second: {vol2} × {pct2/100} = {vol2 * pct2/100} L\nTotal: {vol1 * pct1/100 + vol2 * pct2/100} / {vol1 + vol2} = {result_pct:.1f}%",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Find amount to mix
            vol1 = random.choice([2, 3, 4])
            pct1 = random.choice([30, 35, 40])
            pct2 = random.choice([60, 70, 80])
            target = random.choice([45, 50, 55])
            x = vol1 * (target - pct1) / (pct2 - target)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"How much of a {pct2}% alcohol solution should be mixed with {vol1} liters of a {pct1}% solution to get a {target}% solution?",
                "answer": f"{x:.2f} liters",
                "solution": f"{pct1/100}×{vol1} + {pct2/100}×x = {target/100}×({vol1} + x)\nSolving: x = {x:.2f} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Two unknowns
            total = random.choice([8, 10, 12])
            pct1 = random.choice([20, 25, 30])
            pct2 = random.choice([50, 60, 70])
            target = random.choice([35, 40, 45])
            x = total * (target - pct1) / (pct2 - pct1)
            y = total - x
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A chemist wants {total} liters of a {target}% solution. She has only {pct1}% and {pct2}% solutions. How much of each should she use?",
                "answer": f"{x:.2f} L of {pct2}%, {y:.2f} L of {pct1}%",
                "solution": f"Let x = {pct2}% solution, y = {pct1}% solution\nx + y = {total}\n{pct2/100}x + {pct1/100}y = {target/100}×{total}\nSolving: x = {x:.2f} L, y = {y:.2f} L",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Add water to existing solution
            vol = random.choice([10, 12, 15])
            pct = random.choice([30, 35, 40])
            water = random.choice([2, 3, 4])
            new_pct = (vol * pct) / (vol + water)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A {vol}-liter solution is {pct}% salt. If {water} liters of pure water are added, what is the new concentration?",
                "answer": f"{new_pct:.1f}%",
                "solution": f"Salt: {vol} × {pct/100} = {vol * pct/100} L\nNew volume: {vol + water} L\nNew %: {vol * pct/100} / {vol + water} = {new_pct:.1f}%",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Find amount of pure substance
            vol1 = random.choice([2, 3, 4])
            pct1 = random.choice([40, 50, 60])
            target = random.choice([65, 70, 75])
            x = vol1 * (target - pct1) / (100 - target)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"{vol1} liters of a {pct1}% acid solution is mixed with x liters of pure acid to get a {target}% acid solution. Find x.",
                "answer": f"{x:.2f} liters",
                "solution": f"Acid: {vol1} × {pct1/100} + x = {target/100}({vol1} + x)\n{vol1 * pct1/100} + x = {target/100 * vol1} + {target/100}x\nx = {x:.2f} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Fraction to percentage
            vol = random.choice([6, 9, 12])
            frac_num = 1
            frac_den = random.choice([3, 4])
            target = 50
            current = vol * frac_num / frac_den
            x = (vol * target/100 - current) / (1 - target/100)
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A {vol}-liter mix is {frac_num}/{frac_den} oil. How much oil must be added to make it {target}% oil?",
                "answer": f"{x:.2f} liters",
                "solution": f"Current oil: {vol} × {frac_num}/{frac_den} = {current} L\n({current} + x) / ({vol} + x) = {target/100}\nx = {x:.2f} liters",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Drain and replace
            vol = random.choice([15, 20, 25])
            pct = random.choice([35, 40, 45])
            drained = random.choice([4, 5, 6])
            new_pct = (vol * pct/100 - drained * pct/100) / vol * 100
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A tank has a {vol}-liter mixture that is {pct}% vinegar. If {drained} liters are drained and replaced with water, what is the new concentration?",
                "answer": f"{new_pct:.1f}%",
                "solution": f"Vinegar: {vol} × {pct/100} = {vol * pct/100} L\nRemoved: {drained} × {pct/100} = {drained * pct/100} L\nRemaining: {vol * pct/100 - drained * pct/100} / {vol} = {new_pct:.1f}%",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


def generate_packet3_sectionB(packet_num: int, section: str, count: int) -> List[Dict]:
    """Density Problems"""
    problems = []
    templates = 10
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Basic density calculation
            mass = random.choice([150, 200, 250, 300])
            volume = random.choice([40, 50, 60, 75])
            density = mass / volume
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A metal block has mass {mass} g and volume {volume} cm³. What is its density?",
                "answer": f"{density:.1f} g/cm³",
                "solution": f"Density = Mass / Volume = {mass} / {volume} = {density:.1f} g/cm³",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Find volume from density and mass
            density = random.choice([1.5, 2, 2.5, 3])
            mass = random.choice([300, 400, 500, 600])
            volume = mass / density
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"An object has a density of {density} g/cm³ and a mass of {mass} g. What is its volume?",
                "answer": f"{volume:.0f} cm³",
                "solution": f"Volume = Mass / Density = {mass} / {density} = {volume:.0f} cm³",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Water displacement
            mass = random.choice([120, 150, 180, 200])
            volume = random.choice([50, 60, 75, 80])
            density = mass / volume
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A {mass} g rock displaces {volume} cm³ of water. What is its density?",
                "answer": f"{density:.2f} g/cm³",
                "solution": f"Volume of rock = volume displaced = {volume} cm³\nDensity = {mass} / {volume} = {density:.2f} g/cm³",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Cube density
            side = random.choice([2, 3, 4])
            mass = random.choice([160, 216, 270, 320])
            volume = side ** 3
            density = mass / volume
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A cube has side length {side} cm and mass {mass} g. Find the density.",
                "answer": f"{density:.1f} g/cm³",
                "solution": f"Volume = {side}³ = {volume} cm³\nDensity = {mass} / {volume} = {density:.1f} g/cm³",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Find mass from density and volume
            density = random.choice([0.8, 1.2, 1.5, 2])
            volume = random.choice([200, 250, 300])
            mass = density * volume
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A liquid has a density of {density} g/mL. What is the mass of {volume} mL?",
                "answer": f"{mass:.0f} g",
                "solution": f"Mass = Density × Volume = {density} × {volume} = {mass:.0f} g",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Find mass from density and volume (solid)
            density = random.choice([4, 5, 6, 7])
            volume = random.choice([30, 40, 50])
            mass = density * volume
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"An object has density {density} g/cm³ and volume {volume} cm³. Find the mass.",
                "answer": f"{mass:.0f} g",
                "solution": f"Mass = Density × Volume = {density} × {volume} = {mass:.0f} g",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Compare densities
            mass_a = random.choice([80, 100, 120])
            vol_a = random.choice([20, 25, 30])
            mass_b = random.choice([90, 110, 130])
            vol_b = random.choice([22, 27, 32])
            dens_a = mass_a / vol_a
            dens_b = mass_b / vol_b
            denser = "A" if dens_a > dens_b else "B" if dens_b > dens_a else "Neither"
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Two objects: Object A has mass {mass_a} g and volume {vol_a} cm³. Object B has mass {mass_b} g and volume {vol_b} cm³. Which is denser?",
                "answer": f"Object {denser}" if denser != "Neither" else "Same density",
                "solution": f"Density A: {mass_a} / {vol_a} = {dens_a:.2f} g/cm³\nDensity B: {mass_b} / {vol_b} = {dens_b:.2f} g/cm³\nObject {denser} is denser" if denser != "Neither" else "Same density",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Hollow object
            outer_vol = random.choice([80, 100, 120])
            cavity = random.choice([15, 20, 25])
            mass = random.choice([150, 180, 200])
            material_vol = outer_vol - cavity
            density = mass / material_vol
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A hollow object has outer volume {outer_vol} cm³ and mass {mass} g. If it has an inner cavity of {cavity} cm³, what's its density?",
                "answer": f"{density:.2f} g/cm³",
                "solution": f"Material volume = {outer_vol} - {cavity} = {material_vol} cm³\nDensity = {mass} / {material_vol} = {density:.2f} g/cm³",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Floating/sinking
            floats_in = random.choice(["water", "oil", "alcohol"])
            sinks_in = random.choice(["mercury", "saltwater", "glycerin"])
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A ball floats in {floats_in} but sinks in {sinks_in}. Which has higher density: the ball or {sinks_in}?",
                "answer": f"{sinks_in.capitalize()}",
                "solution": f"An object sinks if it's denser than the fluid. Since the ball sinks in {sinks_in}, {sinks_in} has lower density, so the ball is denser.",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Unit conversion with density
            liters = random.choice([3, 4, 5, 6])
            density = random.choice([0.7, 0.8, 0.9, 1.1])
            ml = liters * 1000
            mass = ml * density
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A tank holds {liters} L of liquid with density {density} g/mL. What is the mass?",
                "answer": f"{mass:.0f} g",
                "solution": f"Volume = {liters} L = {ml} mL\nMass = {density} × {ml} = {mass:.0f} g",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


def generate_packet3_sectionC(packet_num: int, section: str, count: int) -> List[Dict]:
    """Sequence Problems"""
    problems = []
    templates = 10
    
    for i in range(count):
        template_idx = i % templates
        variant_num = i + 1
        
        if template_idx == 0:  # Arithmetic sequence nth term
            first = random.choice([2, 3, 5])
            diff = random.choice([2, 3, 4, 5])
            n = random.choice([8, 10, 12, 15])
            term = first + (n - 1) * diff
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"What is the {n}th term of the arithmetic sequence: {first}, {first + diff}, {first + 2*diff}, ...?",
                "answer": f"{term}",
                "solution": f"First term = {first}, common difference = {diff}\nnth term = a + (n-1)d = {first} + ({n}-1)×{diff} = {term}",
                "source": f"Packet {packet_num}, Section {section}, Template 1"
            })
        
        elif template_idx == 1:  # Sum of arithmetic sequence
            first = random.choice([1, 2, 3])
            diff = random.choice([2, 3, 4])
            n = random.choice([15, 20, 25])
            last = first + (n - 1) * diff
            sum_val = n * (first + last) // 2
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Find the sum of the first {n} terms of {first}, {first + diff}, {first + 2*diff}, ...?",
                "answer": f"{sum_val}",
                "solution": f"First = {first}, d = {diff}, n = {n}\nLast = {first} + ({n}-1)×{diff} = {last}\nSum = (n/2)(first + last) = {n//2}×({first}+{last}) = {sum_val}",
                "source": f"Packet {packet_num}, Section {section}, Template 2"
            })
        
        elif template_idx == 2:  # Geometric sequence nth term
            first = random.choice([2, 3, 5])
            ratio = random.choice([2, 3])
            n = random.choice([5, 6, 7])
            term = first * (ratio ** (n - 1))
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"What is the {n}th term of the geometric sequence: {first}, {first * ratio}, {first * ratio**2}, ...?",
                "answer": f"{term}",
                "solution": f"First = {first}, ratio = {ratio}\n{n}th term = a × r^(n-1) = {first} × {ratio}^{n-1} = {term}",
                "source": f"Packet {packet_num}, Section {section}, Template 3"
            })
        
        elif template_idx == 3:  # Formula-based sequence
            coef = random.choice([2, 3, 4, 5])
            n = random.choice([4, 5, 6])
            term = coef * n * n
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A sequence is defined as aₙ = {coef}n². What is a_{n}?",
                "answer": f"{term}",
                "solution": f"a_{n} = {coef}×{n}² = {coef}×{n*n} = {term}",
                "source": f"Packet {packet_num}, Section {section}, Template 4"
            })
        
        elif template_idx == 4:  # Find which term
            first = random.choice([3, 5, 7])
            diff = random.choice([3, 4, 5])
            target = random.choice([30, 35, 40, 45])
            n = (target - first) // diff + 1
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"In the sequence {first}, {first + diff}, {first + 2*diff},..., which term is {target}?",
                "answer": f"{n}th term",
                "solution": f"a = {first}, d = {diff}\naₙ = a + (n-1)d → {first} + (n-1)×{diff} = {target}\nn = {n}",
                "source": f"Packet {packet_num}, Section {section}, Template 5"
            })
        
        elif template_idx == 5:  # Sum of multiples
            mult = random.choice([5, 6, 7, 8])
            n = random.choice([8, 10, 12])
            last = mult * n
            sum_val = n * (mult + last) // 2
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Find the sum of the first {n} multiples of {mult}.",
                "answer": f"{sum_val}",
                "solution": f"Sequence: {mult}, {2*mult}, ..., {last}\nSum = (n/2)(first + last) = {n//2}×({mult}+{last}) = {sum_val}",
                "source": f"Packet {packet_num}, Section {section}, Template 6"
            })
        
        elif template_idx == 6:  # Powers of 2
            first = random.choice([1, 2, 3])
            n = random.choice([7, 8, 9])
            term = first * (2 ** (n - 1))
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"A pattern goes: {first}, {first*2}, {first*4}, {first*8}, ... What is the {n}th term?",
                "answer": f"{term}",
                "solution": f"Geometric with r = 2\n{n}th term = {first} × 2^{n-1} = {first} × {2**(n-1)} = {term}",
                "source": f"Packet {packet_num}, Section {section}, Template 7"
            })
        
        elif template_idx == 7:  # Linear formula
            a = random.choice([8, 10, 12])
            b = random.choice([2, 3])
            n = random.choice([3, 4, 5])
            term = a - b * n
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"aₙ = {a} - {b}n. What is a_{n}?",
                "answer": f"{term}",
                "solution": f"a_{n} = {a} - {b}×{n} = {term}",
                "source": f"Packet {packet_num}, Section {section}, Template 8"
            })
        
        elif template_idx == 8:  # Find first term from sum
            n = 5
            sum_val = random.choice([40, 45, 50, 55])
            diff = 2
            # Sum = n/2 * (2a + (n-1)d)
            # sum_val = 5/2 * (2a + 8)
            first = (2 * sum_val / n - (n - 1) * diff) / 2
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"If the sum of {n} terms in a sequence is {sum_val} and each term increases by {diff}, what is the first term?",
                "answer": f"{first:.0f}",
                "solution": f"Sum = (n/2)(2a + (n-1)d)\n{sum_val} = ({n}/2)(2a + {(n-1)*diff})\nSolving: a = {first:.0f}",
                "source": f"Packet {packet_num}, Section {section}, Template 9"
            })
        
        else:  # Decreasing arithmetic
            first = random.choice([90, 95, 100])
            diff = random.choice([-4, -5, -6])
            n = random.choice([12, 15, 18])
            term = first + (n - 1) * diff
            problems.append({
                "id": generate_problem_id(packet_num, section, variant_num),
                "prompt": f"Find the {n}th term of {first}, {first + diff}, {first + 2*diff}, ...",
                "answer": f"{term}",
                "solution": f"a = {first}, d = {diff}\na_{n} = {first} + ({n}-1)×({diff}) = {term}",
                "source": f"Packet {packet_num}, Section {section}, Template 10"
            })
    
    return problems


# Placeholder for remaining packets (4-6) - keeping generic for now
def generate_generic_problems(packet_num: int, section: str, section_name: str, count: int) -> List[Dict]:
    """Generate generic problems for packets 4-6"""
    problems = []
    
    # Create simple template-based problems
    for i in range(count):
        variant_num = i + 1
        template_num = (i % 10) + 1
        
        # Generate basic problem structure
        param1 = random.choice([10, 15, 20, 25, 30, 40, 50])
        param2 = random.choice([2, 3, 4, 5, 6, 8, 10])
        result = param1 * param2
        
        problems.append({
            "id": generate_problem_id(packet_num, section, variant_num),
            "prompt": f"[{section_name}] Problem variant {variant_num}: Given {param1} and {param2}, find the result.",
            "answer": f"{result}",
            "solution": f"Multiply {param1} × {param2} = {result}",
            "source": f"Packet {packet_num}, Section {section}, Template {template_num}"
        })
    
    return problems


# ============================================================================
# Main generation logic
# ============================================================================

def generate_all_problems() -> Dict[str, Any]:
    """Generate all problems for all packets"""
    
    bank = {
        "meta": {
            "generated": datetime.now().isoformat(),
            "generator_version": "1.0",
            "random_seed": RANDOM_SEED,
            "total_packets": 6,
            "total_focus_areas": 18,
            "problems_per_focus_area": 100
        },
        "packets": []
    }
    
    # Parse all packet files
    packet_files = sorted(PACKETS_DIR.glob("Packet*.txt"))
    
    for packet_file in packet_files:
        print(f"Processing {packet_file.name}...")
        packet_info = parse_packet_file(packet_file)
        
        packet_data = {
            "packetNumber": packet_info['packet_num'],
            "title": packet_info['title'],
            "focusAreas": []
        }
        
        # Generate problems for each section
        for section_letter in ['A', 'B', 'C']:
            if section_letter in packet_info['sections']:
                print(f"  Generating Section {section_letter}...")
                section_name = packet_info['sections'][section_letter]
                
                # Route to appropriate generator
                if packet_info['packet_num'] == 1:
                    if section_letter == 'A':
                        problems = generate_packet1_sectionA(packet_info['packet_num'], section_letter, 100)
                    elif section_letter == 'B':
                        problems = generate_packet1_sectionB(packet_info['packet_num'], section_letter, 100)
                    else:  # C
                        problems = generate_packet1_sectionC(packet_info['packet_num'], section_letter, 100)
                elif packet_info['packet_num'] == 2:
                    if section_letter == 'A':
                        problems = generate_packet2_sectionA(packet_info['packet_num'], section_letter, 100)
                    elif section_letter == 'B':
                        problems = generate_packet2_sectionB(packet_info['packet_num'], section_letter, 100)
                    else:  # C
                        problems = generate_packet2_sectionC(packet_info['packet_num'], section_letter, 100)
                elif packet_info['packet_num'] == 3:
                    if section_letter == 'A':
                        problems = generate_packet3_sectionA(packet_info['packet_num'], section_letter, 100)
                    elif section_letter == 'B':
                        problems = generate_packet3_sectionB(packet_info['packet_num'], section_letter, 100)
                    else:  # C
                        problems = generate_packet3_sectionC(packet_info['packet_num'], section_letter, 100)
                else:
                    # For packets 4-6, use generic generator (will implement next)
                    problems = generate_generic_problems(packet_info['packet_num'], section_letter, section_name, 100)
                
                focus_area = {
                    "section": section_letter,
                    "name": section_name,
                    "problems": problems
                }
                
                packet_data["focusAreas"].append(focus_area)
        
        bank["packets"].append(packet_data)
    
    return bank


def main():
    """Main entry point"""
    print("=" * 70)
    print("TJ Math Problem Bank Generator")
    print("=" * 70)
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Random seed: {RANDOM_SEED}")
    print()
    
    bank = generate_all_problems()
    
    # Write to file
    print()
    print("Writing JSON file...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 70)
    print("✓ Generation complete!")
    print("=" * 70)
    print(f"  Total packets: {len(bank['packets'])}")
    total_problems = sum(len(fa['problems']) for p in bank['packets'] for fa in p['focusAreas'])
    print(f"  Total problems: {total_problems}")
    print(f"  Output: {OUTPUT_FILE}")
    print()


if __name__ == "__main__":
    main()
