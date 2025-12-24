# TJ Math Quiz Application

An interactive web-based quiz application for practicing TJ Math problems from the generated problem bank.

**Quick Stats**: 1,800 problems across 6 packets and 18 focus areas, all with complete worked solutions.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Answer Format Tips](#answer-format-tips)
- [Problem Bank Structure](#problem-bank-structure)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)
- [Problem Generation](#problem-generation) - **For developers/future reference**

## Features

- **Focus Area Selection**: Choose from 18 different math focus areas across 6 packets
- **Random Problem Selection**: Get 10 randomly selected problems from your chosen areas
- **Immediate Feedback**: See if your answer is correct right away
- **Detailed Solutions**: View worked solutions for incorrect answers
- **Performance Tracking**: See your score broken down by focus area
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices
- **No Backend Required**: Runs entirely in the browser

## Usage

### Quick Start

1. Make sure `index.html` and `bank.json` are in the same directory
2. Open `index.html` in a web browser

**Note**: Due to browser security restrictions, you may need to serve the files through a local web server rather than opening the file directly. 

### Using a Local Web Server

#### Option 1: Python (recommended)
```bash
cd /path/to/tjmath
python3 -m http.server 8000
```
Then open http://localhost:8000 in your browser.

#### Option 2: Node.js
```bash
npx http-server
```

#### Option 3: PHP
```bash
php -S localhost:8000
```

### How to Use the Quiz

1. **Select Focus Areas**
   - Check the boxes for the math topics you want to practice
   - Use "Select All" to practice all areas at once
   - Click "Start Quiz" when ready

2. **Answer Questions**
   - Read each problem carefully
   - Type your answer in the input field
   - Click "Submit Answer" or press Enter
   - Review the feedback (correct/incorrect)
   - For incorrect answers, study the provided solution
   - Click "Next Problem" to continue

3. **View Results**
   - See your overall score (X/10)
   - Review performance by focus area
   - Click "Try Again" to practice the same areas
   - Click "Change Focus Areas" to select different topics

## Answer Format Tips

The app accepts answers in various formats:
- Numbers: `42`, `3.14`, `0.5`
- With units: `50 mph`, `100 miles`, `2.5 hours`
- Fractions: `1/2`, `3/4`
- Degrees: `45°`, `90 degrees`

The answer checker is flexible and will accept:
- Answers with or without units (if the correct answer includes units)
- Small decimal variations (±0.01)
- Different spacing and capitalization

## Problem Bank Structure

The quiz draws from a bank of 1,800 problems organized as:
- **6 Packets** covering different math topics
- **18 Focus Areas** (3 per packet)
- **100 Problems** per focus area

All problems are algorithmically generated with:
- Random parameters within realistic ranges
- Complete worked solutions showing step-by-step work
- Proper mathematical notation and units
- Unique IDs (format: P{packet}{section}{number}, e.g., P5A042)

### Available Focus Areas

**Packet 1: Distance, Work, and Unit Conversion**
- Distance = Rate × Time
- Work and Rate Problems
- Unit Conversions & Applied Problems

**Packet 2: Ratios, Linear Equations, and Area/Volume**
- Ratios, Proportions, Percents
- Linear Equations & Word Problems
- Area, Volume, and Geometry

**Packet 3: Mixtures, Density, and Sequences**
- Mixtures
- Density
- Sequences

**Packet 4: Systems of Equations, Pythagorean/Coordinate Geometry, Slope**
- Systems of Equations
- Pythagorean & Coordinate Geometry
- Slope & Linear Equations

**Packet 5: Punnett Squares, Exponential Growth/Decay, and Experimental Design**
- Punnett Squares
- Exponential Growth and Decay
- Experimental Design

**Packet 6: Energy Transfer, Mass vs. Weight, and Clock Problems**
- Energy Transfer (Ecosystems)
- Mass vs. Weight
- Clock Problems

## Technical Details

- **Technology**: Pure HTML, CSS, and JavaScript (no frameworks)
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **File Size**: ~30KB HTML + 588KB JSON data
- **No Dependencies**: Self-contained application
- **Offline Capable**: Works without internet once loaded

## Files

- `index.html` - The complete quiz application
- `bank.json` - Problem bank with 1,800 problems
- `README.md` - This documentation

## Troubleshooting

### "Failed to load problem bank" Error

This usually means the browser couldn't fetch `bank.json`. Solutions:
1. Make sure `bank.json` is in the same directory as `index.html`
2. Use a local web server instead of opening the file directly
3. Check browser console (F12) for specific error messages

### Problems Not Displaying

1. Check that `bank.json` is valid JSON
2. Clear browser cache and reload
3. Try a different browser

### Answer Always Marked Wrong

The answer checker is case-insensitive and flexible with spacing, but:
- Make sure you're entering the answer in a reasonable format
- Check for typos
- Include units if the correct answer shows units
- For fractions, use format like `1/2` not "one half"

## Customization

To modify the quiz behavior, edit `index.html`:

- **Number of problems**: Change `allProblems.slice(0, 10)` to a different number
- **Colors**: Modify the CSS color variables
- **Answer checking**: Adjust the `checkAnswer()` function
- **Styling**: Edit the `<style>` section

## Problem Generation

### Overview

All 1,800 problems are generated by `scripts/generate_bank.py`, which creates unique problem variants with randomized parameters while maintaining mathematical correctness.

### Generation Process

1. **Parse Source Packets**: Read the 6 original TJ Math packet text files from the `packets/` directory
2. **Extract Structure**: Identify packet numbers, titles, sections, and problem types
3. **Generate Variants**: Create 100 unique problems per focus area using templates
4. **Solve Problems**: Calculate correct answers and generate step-by-step solutions
5. **Output JSON**: Save to `bank.json` in structured format

### Problem Templates

Each focus area has 10 different problem templates that cycle through the 100 problems. Templates vary:
- Parameter ranges (e.g., speeds from 40-80 mph, distances from 50-500 miles)
- Problem contexts (cars, trains, planes, runners, cyclists)
- Complexity levels (single-step to multi-step problems)
- Units and formats (metric/imperial, fractions/decimals)

### Key Implementation Details

**Packet 1: Distance, Work, Unit Conversion**
- Distance problems: Vary speed (40-80 mph), time (1-8 hours), calculate distance or solve for unknowns
- Work problems: Multiple workers with different rates, combined work, time to completion
- Unit conversions: Length, volume, weight, temperature with multi-step conversions

**Packet 2: Ratios, Linear Equations, Geometry**
- Ratios: Part-to-part, part-to-whole, scaling, proportions with real-world contexts
- Linear equations: Solve for x, word problems (age, money, consecutive numbers)
- Geometry: Area (rectangles, triangles, circles), volume (boxes, cylinders, spheres), perimeter

**Packet 3: Mixtures, Density, Sequences**
- Mixtures: Concentration problems, combining solutions, dilution, alloy mixing
- Density: Mass/volume calculations, object identification, buoyancy
- Sequences: Arithmetic (find nth term, sum), geometric (growth patterns), pattern recognition

**Packet 4: Systems, Pythagorean, Slope**
- Systems: Substitution and elimination methods, word problems (tickets, coins)
- Pythagorean: Right triangles, distance formula, coordinate geometry
- Slope: Calculate from points, parallel/perpendicular lines, point-slope form

**Packet 5: Punnett Squares, Exponential, Experimental Design**
- Punnett Squares: Monohybrid/dihybrid crosses, X-linked traits, blood types, incomplete dominance
- Exponential: Bacterial growth (doubling/tripling), radioactive decay (half-life), compound interest, population growth
- Experimental Design: Variables, controls, confounding factors, correlation vs causation, reliability

**Packet 6: Energy Transfer, Mass vs Weight, Clock Problems**
- Energy Transfer: 10% rule, trophic levels, food chains, ecosystem efficiency
- Mass vs Weight: Weight = mass × gravity, conversions between planets, gravitational acceleration
- Clock Problems: Angle calculations (hour/minute hands), hands coinciding/opposite, fast/slow clocks

### Data Structure

Each problem in `bank.json` follows this structure:

```json
{
  "id": "P5A042",
  "prompt": "Problem text with specific parameters...",
  "answer": "Correct answer with units",
  "solution": "Step-by-step solution showing work...",
  "source": "Packet 5, Section A"
}
```

### Regenerating Problems

To regenerate the problem bank with different random parameters:

```bash
cd /Users/vsokolov/www/html/tjmath
python3 scripts/generate_bank.py
```

This will:
- Use seed 42 for reproducibility (change `random.seed(42)` for different variants)
- Generate all 1,800 problems from scratch
- Overwrite `bank.json` with new problem set
- Take approximately 2-3 seconds to complete

### Adding New Problem Types

To add new problem templates:

1. Open `scripts/generate_bank.py`
2. Find the relevant packet function (e.g., `packet5_punnett()`)
3. Add new template in the `if template == X:` section
4. Ensure proper parameter randomization and solution calculation
5. Run generator to test new problems

### Template Pattern

Each problem generator follows this pattern:

```python
def packet_section(packet, section, count):
    problems = []
    for i in range(count):
        variant = i + 1
        template = i % 10  # Cycle through 10 templates
        
        if template == 0:
            # Generate parameters
            param1 = random.choice([...])
            param2 = random.randint(...)
            
            # Calculate answer
            answer = calculate(param1, param2)
            
            # Create problem
            problems.append({
                "id": generate_problem_id(packet, section, variant),
                "prompt": f"Problem text with {param1} and {param2}...",
                "answer": f"{answer} units",
                "solution": f"Step 1: ...\nStep 2: ...\nAnswer: {answer}",
                "source": f"Packet {packet}, Section {section}"
            })
    return problems
```

### Quality Assurance

All generated problems are validated for:
- Mathematical correctness (answers match solutions)
- Unique IDs (no duplicates)
- Proper formatting (units, notation)
- Realistic parameters (no negative distances, reasonable ranges)
- Complete solutions (all steps shown)

### Random Seed

The generator uses `random.seed(42)` for reproducibility. This ensures:
- Same problems generated each time
- Consistent testing and validation
- Predictable problem distribution

To generate different problem sets, change the seed value or remove the seed line for truly random generation.

## License

This quiz application is part of the TJ Math practice materials.

## Support

For issues or questions:
1. Check this README
2. Review the browser console for errors
3. Verify file locations and web server setup

