# TJ Math Quiz Application

An interactive web-based quiz application for practicing TJ Math problems from the generated problem bank.

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

## License

This quiz application is part of the TJ Math practice materials.

## Support

For issues or questions:
1. Check this README
2. Review the browser console for errors
3. Verify file locations and web server setup

