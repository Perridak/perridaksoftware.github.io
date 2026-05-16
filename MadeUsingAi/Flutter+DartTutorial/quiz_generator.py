#!/usr/bin/env python3
"""
Knowledge Check Quiz Generator v2
Converts 12-KnowledgeCheck.txt to a complete HTML quiz page.

Usage:
    python3 quiz_generator_v2.py [input_file] [output_file]

Default files:
    Input:  12-KnowledgeCheck.txt
    Output: 12-KnowledgeCheck.html

Question Format (in .txt file):
    Question text here?
    A) First option
    B) Second option
    C) Third option
    D) Fourth option
    A
    
    [blank line between questions]

Answer Key: Single letter (A, B, C, or D) on its own line after options.
"""

import sys
import re


def parse_questions(input_file):
    """Parse questions from text file and return list of question dicts."""
    import random
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    # Split by double newlines (question blocks)
    blocks = content.split('\n\n')
    questions = []
    
    for block_num, block in enumerate(blocks, 1):
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        
        # Each block should have: question, 4 options, answer
        if len(lines) < 6:
            print(f"Warning: Block {block_num} has only {len(lines)} lines (skipping)")
            continue
        
        question = lines[0]
        options = []
        answer_key = None
        
        # Parse options (lines 1-4, format: "A) Option text")
        for i in range(1, 5):
            if i < len(lines) and len(lines[i]) > 2:
                if lines[i][0] in 'ABCD' and lines[i][1] == ')':
                    option_text = lines[i][3:].strip()
                    options.append(option_text)
        
        # Parse answer (line 5, single letter A/B/C/D)
        if len(lines) > 5 and lines[5] in ['A', 'B', 'C', 'D']:
            answer_key = ord(lines[5]) - ord('A')
        
        # Validate block
        if len(options) != 4:
            print(f"Warning: Block {block_num} has {len(options)} options (expected 4)")
            continue
        
        if answer_key is None:
            print(f"Warning: Block {block_num} has no valid answer key")
            continue
        
        # Create list of (option_text, original_index) tuples
        indexed_options = [(opt, idx) for idx, opt in enumerate(options)]
        
        # Shuffle the options
        random.shuffle(indexed_options)
        
        # Extract shuffled options and find new correct answer position
        shuffled_options = [opt[0] for opt in indexed_options]
        new_correct_index = next(idx for idx, (opt, orig_idx) in enumerate(indexed_options) if orig_idx == answer_key)
        
        questions.append({
            'question': question,
            'options': shuffled_options,
            'correctIndex': new_correct_index
        })
    
    return questions


def escape_html(text):
    """Escape special characters for HTML."""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text


def escape_js_string(text):
    """Escape special characters for JavaScript string literals."""
    text = text.replace('\\', '\\\\')
    text = text.replace('"', '\\"')
    text = text.replace('\n', '\\n')
    return text


def generate_html_file(questions):
    """Generate complete HTML quiz page with embedded questions."""
    
    # JavaScript question pool
    js_pool = "    const questionPool = [\n"
    
    for q in questions:
        q_escaped = escape_js_string(q['question'])
        opts_escaped = [escape_js_string(opt) for opt in q['options']]
        opts_str = ', '.join([f'"{opt}"' for opt in opts_escaped])
        
        js_pool += f'        {{ question: "{q_escaped}", options: [{opts_str}], correctIndex: {q["correctIndex"]} }},\n'
    
    js_pool += "    ];\n"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge Check Quiz - 200 Questions</title>
    <link rel="stylesheet" href="common.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #3D4A52;
            background: transparent;
            padding: 2rem;
        }}
        
        .quiz-container {{
            max-width: 700px;
            margin: 0 auto;
        }}
        
        .quiz-header {{
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .quiz-header h1 {{
            color: #1B5A56;
            font-size: 2.5rem;
            border-bottom: 3px solid #7BA857;
            padding-bottom: 0.75rem;
            margin-bottom: 1rem;
        }}
        
        .quiz-header p {{
            color: #5A7A72;
            font-size: 1.1rem;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background-color: #E8F0E6;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 1.5rem;
        }}
        
        .progress-fill {{
            height: 100%;
            background-color: #7BA857;
            transition: width 0.3s ease;
        }}
        
        .progress-text {{
            text-align: center;
            font-size: 0.9rem;
            color: #5A7A72;
            margin-bottom: 1rem;
        }}
        
        .quiz-question {{
            margin-bottom: 2rem;
        }}
        
        .question-text {{
            font-weight: 600;
            color: #1B5A56;
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }}
        
        .options {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        
        .option {{
            padding: 1rem;
            border: 2px solid #D4DED7;
            border-radius: 6px;
            background: white;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
        }}
        
        .option:hover {{
            border-color: #7BA857;
            background: #F9F7F3;
        }}
        
        .option input[type="radio"] {{
            margin-right: 0.75rem;
            cursor: pointer;
        }}
        
        .option.selected {{
            background: #E8F0E6;
            border-color: #7BA857;
        }}
        
        .option.correct {{
            background: #D4E5D0;
            border-color: #7BA857;
        }}
        
        .option.incorrect {{
            background: #F5D5D5;
            border-color: #D66767;
        }}
        
        .button-group {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }}
        
        button {{
            padding: 0.75rem 2rem;
            font-size: 1rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .btn-next {{
            background-color: #7BA857;
            color: white;
        }}
        
        .btn-next:hover:not(:disabled) {{
            background-color: #6B9647;
        }}
        
        .btn-next:disabled {{
            background-color: #B0C8A8;
            cursor: not-allowed;
        }}
        
        #quizContent {{
            display: block;
        }}
        
        #resultsContent {{
            display: none;
        }}
        
        #resultsContent.show {{
            display: block;
        }}
        
        .results {{
            text-align: center;
        }}
        
        .results h2 {{
            color: #1B5A56;
            font-size: 2rem;
            margin-bottom: 1rem;
        }}
        
        .score {{
            font-size: 3rem;
            color: #7BA857;
            font-weight: bold;
            margin: 1rem 0;
        }}
        
        .score-details {{
            color: #5A7A72;
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }}
        
        .btn-restart {{
            background-color: #1B5A56;
            color: white;
            margin-top: 1.5rem;
        }}
        
        .btn-restart:hover {{
            background-color: #154A47;
        }}
    </style>
</head>
<body>
<div class="quiz-container">
    <div class="quiz-header">
        <h1>Knowledge Check Quiz</h1>
        <p>Test your understanding of Flutter and Dart fundamentals</p>
    </div>
    
    <div id="quizContent">
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
        <div class="progress-text" id="progressText">0/15</div>
        
        <div id="questionContainer" class="quiz-question"></div>
        
        <div class="button-group">
            <button id="nextBtn" class="btn-next" disabled>Next Question</button>
        </div>
    </div>
    
    <div id="resultsContent" class="results">
        <h2>Quiz Complete!</h2>
        <p>Your score:</p>
        <div class="score" id="scoreDisplay">0%</div>
        <p class="score-details" id="scoreDetails">0 out of 15 correct</p>
        <button id="restartBtn" class="btn-restart">Take Another Quiz</button>
    </div>
</div>

<script>
{js_pool}
    const questionsPerSession = 15;
    
    function getRandomQuestions() {{
        const shuffled = [...questionPool].sort(() => Math.random() - 0.5);
        return shuffled.slice(0, questionsPerSession);
    }}
    
    let currentQuestions = [];
    let currentIndex = 0;
    let score = 0;
    
    function init() {{
        currentQuestions = getRandomQuestions();
        currentIndex = 0;
        score = 0;
        document.getElementById('quizContent').style.display = 'block';
        document.getElementById('resultsContent').classList.remove('show');
        showQuestion();
    }}
    
    function showQuestion() {{
        const question = currentQuestions[currentIndex];
        const container = document.getElementById('questionContainer');
        
        let html = `<div class="question-text">${{currentIndex + 1}}. ${{question.question}}</div>`;
        html += '<div class="options">';
        
        question.options.forEach((option, idx) => {{
            const id = `option${{idx}}`;
            html += `
                <label class="option" onclick="selectOption(this, ${{idx}})">
                    <input type="radio" id="${{id}}" name="answer" value="${{idx}}" />
                    ${{option}}
                </label>
            `;
        }});
        
        html += '</div>';
        container.innerHTML = html;
        
        updateProgress();
    }}
    
    function selectOption(element, index) {{
        // Remove previously selected option styling
        document.querySelectorAll('.option').forEach(opt => {{
            opt.classList.remove('selected', 'correct', 'incorrect');
        }});
        
        // Mark the selected option
        element.classList.add('selected');
        
        // Get the correct answer for this question
        const correctAnswer = currentQuestions[currentIndex].correctIndex;
        const userAnswer = index;
        
        // Provide immediate feedback
        if (userAnswer === correctAnswer) {{
            element.classList.add('correct');
        }} else {{
            element.classList.add('incorrect');
            // Also highlight the correct answer in green
            document.querySelectorAll('.option').forEach((opt, idx) => {{
                if (idx === correctAnswer) {{
                    opt.classList.add('correct');
                }}
            }});
        }}
        
        document.getElementById('nextBtn').disabled = false;
    }}
    
    function nextQuestion() {{
        const selected = document.querySelector('.option.selected input');
        if (!selected) return;
        
        const userAnswer = parseInt(selected.value);
        const correctAnswer = currentQuestions[currentIndex].correctIndex;
        
        if (userAnswer === correctAnswer) {{
            score++;
        }}
        
        currentIndex++;
        
        if (currentIndex < currentQuestions.length) {{
            document.getElementById('nextBtn').disabled = true;
            showQuestion();
        }} else {{
            showResults();
        }}
    }}
    
    function updateProgress() {{
        const progress = ((currentIndex) / currentQuestions.length) * 100;
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('progressText').textContent = `${{currentIndex}}/${{currentQuestions.length}}`;
    }}
    
    function showResults() {{
        document.getElementById('quizContent').style.display = 'none';
        document.getElementById('resultsContent').classList.add('show');
        
        const percentage = Math.round((score / currentQuestions.length) * 100);
        document.getElementById('scoreDisplay').textContent = percentage + '%';
        document.getElementById('scoreDetails').textContent = `${{score}} out of ${{currentQuestions.length}} correct`;
    }}
    
    document.getElementById('nextBtn').addEventListener('click', nextQuestion);
    document.getElementById('restartBtn').addEventListener('click', init);
    
    // Initialize on page load
    window.addEventListener('load', init);
</script>
</body>
</html>"""
    
    return html


def main():
    """Main entry point."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = '12-KnowledgeCheck.txt'
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = '12-KnowledgeCheck.html'
    
    print(f"Reading questions from: {input_file}")
    
    try:
        questions = parse_questions(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)
    
    if not questions:
        print("Error: No valid questions found in file")
        sys.exit(1)
    
    print(f"✓ Parsed {len(questions)} questions")
    
    # Generate HTML output
    html_output = generate_html_file(questions)
    
    # Write output
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_output)
        print(f"✓ HTML quiz written to: {output_file}")
        print(f"✓ Generated complete quiz with {len(questions)} questions")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
