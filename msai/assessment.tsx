import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, CheckCircle, Code, Calculator, BarChart3 } from 'lucide-react';

const AssessmentTool = () => {
  const [currentSection, setCurrentSection] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [studentName, setStudentName] = useState('');
  const [studentEmail, setStudentEmail] = useState('');
  const [hasStarted, setHasStarted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  const sections = [
    {
      id: 'programming',
      title: 'Programming Fundamentals',
      icon: Code,
      description: 'Arrays, loops, classes in Python/R',
      questions: [
        {
          id: 'p1',
          type: 'code',
          language: 'python',
          question: 'What will this Python code output?',
          code: `numbers = [1, 2, 3, 4, 5]
result = [x * 2 for x in numbers if x % 2 == 0]
print(result)`,
          options: ['[2, 4, 6, 8, 10]', '[4, 8]', '[2, 4]', '[1, 2, 3, 4, 5]'],
          correct: 1
        },
        {
          id: 'p2',
          type: 'code',
          language: 'python',
          question: 'Complete the class method to calculate the area of a rectangle:',
          code: `class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        # Complete this method
        return ___________`,
          options: [
            'self.width + self.height',
            'self.width * self.height',
            'self.width ** self.height',
            'width * height'
          ],
          correct: 1
        },
        {
          id: 'p3',
          type: 'code',
          language: 'r',
          question: 'In R, which function correctly applies a function to each element of a vector?',
          options: [
            'apply(vector, function)',
            'sapply(vector, function)',
            'map(function, vector)',
            'forEach(vector, function)'
          ],
          correct: 1
        },
        {
          id: 'p4',
          type: 'code',
          language: 'python',
          question: 'What is the time complexity of accessing an element in an array by index?',
          options: ['O(n)', 'O(log n)', 'O(1)', 'O(n²)'],
          correct: 2
        }
      ]
    },
    {
      id: 'calculus',
      title: 'Calculus Basics',
      icon: Calculator,
      description: 'Derivatives, gradients, integrals',
      questions: [
        {
          id: 'c1',
          type: 'math',
          question: 'What is the derivative of f(x) = 3x² + 2x + 1?',
          options: ['6x + 2', '3x + 2', '6x² + 2x', '3x² + 2'],
          correct: 0
        },
        {
          id: 'c2',
          type: 'math',
          question: 'For a function f(x,y) = x²y + y³, what is ∂f/∂x (partial derivative with respect to x)?',
          options: ['2xy + 3y²', '2xy', 'x² + 3y²', '2x + y³'],
          correct: 1
        },
        {
          id: 'c3',
          type: 'math',
          question: 'What is the gradient of f(x,y) = x² + y² at point (1,1)?',
          options: ['(2, 2)', '(1, 1)', '(0, 0)', '(2, 0)'],
          correct: 0
        },
        {
          id: 'c4',
          type: 'math',
          question: 'What is ∫(2x + 3)dx?',
          options: ['2x² + 3x + C', 'x² + 3x + C', '2x + C', 'x² + 3 + C'],
          correct: 1
        },
        {
          id: 'c5',
          type: 'math',
          question: 'In gradient descent, the gradient points in the direction of:',
          options: [
            'Steepest ascent',
            'Steepest descent',
            'Local minimum',
            'Global minimum'
          ],
          correct: 0
        }
      ]
    },
    {
      id: 'probability',
      title: 'Probability & Data Analysis',
      icon: BarChart3,
      description: 'Probability, statistics, data manipulation',
      questions: [
        {
          id: 'pr1',
          type: 'concept',
          question: 'If P(A) = 0.3 and P(B) = 0.4, and A and B are independent, what is P(A ∩ B)?',
          options: ['0.7', '0.12', '0.1', '0.4'],
          correct: 1
        },
        {
          id: 'pr2',
          type: 'code',
          language: 'python',
          question: 'Which Pandas function loads a CSV file into a DataFrame?',
          code: 'import pandas as pd\ndf = pd.________("data.csv")',
          options: ['read_csv', 'load_csv', 'import_csv', 'open_csv'],
          correct: 0
        },
        {
          id: 'pr3',
          type: 'concept',
          question: 'Which measure is most robust to outliers?',
          options: ['Mean', 'Median', 'Standard deviation', 'Range'],
          correct: 1
        },
        {
          id: 'pr4',
          type: 'code',
          language: 'python',
          question: 'What does this code calculate?',
          code: `import numpy as np
data = [1, 2, 3, 4, 5]
result = np.std(data)`,
          options: [
            'Mean',
            'Variance',
            'Standard deviation',
            'Median'
          ],
          correct: 2
        },
        {
          id: 'pr5',
          type: 'concept',
          question: 'What is the expected value of a fair six-sided die?',
          options: ['3', '3.5', '4', '6'],
          correct: 1
        }
      ]
    }
  ];

  const handleAnswer = (questionId, answerIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }));
  };

  const calculateResults = () => {
    const results = {};
    let totalCorrect = 0;
    let totalQuestions = 0;

    sections.forEach(section => {
      let sectionCorrect = 0;
      section.questions.forEach(q => {
        totalQuestions++;
        if (answers[q.id] === q.correct) {
          sectionCorrect++;
          totalCorrect++;
        }
      });
      results[section.id] = {
        correct: sectionCorrect,
        total: section.questions.length,
        percentage: Math.round((sectionCorrect / section.questions.length) * 100)
      };
    });

    results.overall = {
      correct: totalCorrect,
      total: totalQuestions,
      percentage: Math.round((totalCorrect / totalQuestions) * 100)
    };

    return results;
  };

  const getRecommendations = (results) => {
    const recs = [];
    
    if (results.programming.percentage < 70) {
      recs.push({
        area: 'Programming',
        recommendation: 'Review Python/R fundamentals, practice with list comprehensions, and strengthen OOP concepts.'
      });
    }
    
    if (results.calculus.percentage < 70) {
      recs.push({
        area: 'Calculus',
        recommendation: 'Brush up on derivatives, gradients, and chain rule. Khan Academy calculus courses recommended.'
      });
    }
    
    if (results.probability.percentage < 70) {
      recs.push({
        area: 'Probability & Data',
        recommendation: 'Practice probability basics and get comfortable with Pandas/NumPy for data manipulation.'
      });
    }

    if (recs.length === 0) {
      recs.push({
        area: 'Overall',
        recommendation: 'Great job! You have a solid foundation for the AI program.'
      });
    }

    return recs;
  };

  const submitAssessment = async (results, recommendations) => {
    setIsSubmitting(true);
    setSubmitMessage('');

    try {
      const response = await fetch('http://localhost:3001/api/submit-assessment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          studentName,
          studentEmail,
          answers,
          results,
          recommendations,
          sections,
        }),
      });

      const data = await response.json();
      
      if (data.success) {
        setSubmitMessage('✓ Report sent to your email successfully!');
      } else {
        setSubmitMessage('✗ Failed to send report. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting assessment:', error);
      setSubmitMessage('✗ Error connecting to server. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const currentSectionData = sections[currentSection];
  const Icon = currentSectionData.icon;

  if (showResults) {
    const results = calculateResults();
    const recommendations = getRecommendations(results);

    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
        <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Assessment Complete!</h1>
            <p className="text-gray-600">Here are your results, {studentName}</p>
          </div>

          <div className="mb-8">
            <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white mb-6">
              <div className="text-center">
                <div className="text-5xl font-bold mb-2">{results.overall.percentage}%</div>
                <div className="text-xl">Overall Score</div>
                <div className="text-sm opacity-90 mt-2">
                  {results.overall.correct} out of {results.overall.total} correct
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              {sections.map(section => {
                const sectionResult = results[section.id];
                const SectionIcon = section.icon;
                return (
                  <div key={section.id} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <div className="flex items-center mb-2">
                      <SectionIcon className="w-5 h-5 text-indigo-600 mr-2" />
                      <h3 className="font-semibold text-gray-800">{section.title}</h3>
                    </div>
                    <div className="text-3xl font-bold text-indigo-600 mb-1">
                      {sectionResult.percentage}%
                    </div>
                    <div className="text-sm text-gray-600">
                      {sectionResult.correct}/{sectionResult.total} correct
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Recommendations</h3>
              <div className="space-y-3">
                {recommendations.map((rec, idx) => (
                  <div key={idx} className="flex items-start">
                    <div className="w-2 h-2 bg-amber-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                    <div>
                      <div className="font-medium text-gray-800">{rec.area}</div>
                      <div className="text-gray-600 text-sm">{rec.recommendation}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <button
              onClick={() => submitAssessment(results, recommendations)}
              disabled={isSubmitting}
              className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isSubmitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending Report...
                </>
              ) : (
                'Email Detailed Report (PDF)'
              )}
            </button>

            {submitMessage && (
              <div className={`p-4 rounded-lg text-center ${
                submitMessage.includes('✓') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
              }`}>
                {submitMessage}
              </div>
            )}

            <button
              onClick={() => {
                setShowResults(false);
                setCurrentSection(0);
                setAnswers({});
                setStudentName('');
                setStudentEmail('');
                setHasStarted(false);
                setSubmitMessage('');
              }}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Take Assessment Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!hasStarted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6 flex items-center justify-center">
        <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Program Assessment</h1>
          <p className="text-gray-600 mb-6">
            This assessment will evaluate your readiness in programming, calculus, and probability/statistics.
          </p>
          
          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
              <input
                type="text"
                value={studentName}
                onChange={(e) => setStudentName(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Enter your name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={studentEmail}
                onChange={(e) => setStudentEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Enter your email"
              />
            </div>
          </div>

          <button
            onClick={() => {
              if (studentName) {
                setHasStarted(true);
              }
            }}
            disabled={!studentName}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Start Assessment
          </button>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-600 mb-3">This assessment covers:</p>
            <ul className="space-y-2">
              {sections.map(section => {
                const SectionIcon = section.icon;
                return (
                  <li key={section.id} className="flex items-center text-sm text-gray-700">
                    <SectionIcon className="w-4 h-4 mr-2 text-indigo-600" />
                    {section.title} ({section.questions.length} questions)
                  </li>
                );
              })}
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Icon className="w-8 h-8 text-indigo-600 mr-3" />
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">{currentSectionData.title}</h2>
                  <p className="text-gray-600 text-sm">{currentSectionData.description}</p>
                </div>
              </div>
              <div className="text-sm text-gray-500">
                Section {currentSection + 1} of {sections.length}
              </div>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentSection + 1) / sections.length) * 100}%` }}
              ></div>
            </div>
          </div>

          <div className="space-y-6">
            {currentSectionData.questions.map((question, qIdx) => (
              <div key={question.id} className="border border-gray-200 rounded-lg p-6 bg-gray-50">
                <div className="mb-4">
                  <div className="flex items-start mb-3">
                    <span className="bg-indigo-600 text-white rounded-full w-7 h-7 flex items-center justify-center text-sm font-semibold mr-3 flex-shrink-0">
                      {qIdx + 1}
                    </span>
                    <p className="text-gray-800 font-medium">{question.question}</p>
                  </div>

                  {question.code && (
                    <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg text-sm overflow-x-auto mb-4 font-mono">
                      {question.code}
                    </pre>
                  )}
                </div>

                <div className="space-y-2">
                  {question.options.map((option, optIdx) => (
                    <button
                      key={optIdx}
                      onClick={() => handleAnswer(question.id, optIdx)}
                      className={`w-full text-left p-4 rounded-lg border-2 transition-all ${
                        answers[question.id] === optIdx
                          ? 'border-indigo-600 bg-indigo-50'
                          : 'border-gray-200 hover:border-indigo-300 bg-white'
                      }`}
                    >
                      <div className="flex items-center">
                        <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                          answers[question.id] === optIdx
                            ? 'border-indigo-600 bg-indigo-600'
                            : 'border-gray-300'
                        }`}>
                          {answers[question.id] === optIdx && (
                            <div className="w-2 h-2 bg-white rounded-full"></div>
                          )}
                        </div>
                        <span className={`font-mono text-sm ${
                          answers[question.id] === optIdx ? 'text-indigo-900' : 'text-gray-700'
                        }`}>
                          {option}
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="flex justify-between mt-8">
            <button
              onClick={() => setCurrentSection(prev => prev - 1)}
              disabled={currentSection === 0}
              className="flex items-center px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-5 h-5 mr-1" />
              Previous
            </button>

            {currentSection === sections.length - 1 ? (
              <button
                onClick={() => setShowResults(true)}
                className="flex items-center px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Submit Assessment
                <CheckCircle className="w-5 h-5 ml-2" />
              </button>
            ) : (
              <button
                onClick={() => setCurrentSection(prev => prev + 1)}
                className="flex items-center px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Next
                <ChevronRight className="w-5 h-5 ml-1" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssessmentTool;