import { useEffect, useState } from "react";

type Question = {
    question_id: string
    type: 'numeric' | 'choice'
    prompt: string
    choices: string[] | null
}

type Result = { correct: boolean; explanation?: string; stage: number }

type Props = { skillId: string; onStage: (stage: number) => void }

function Practice({ skillId, onStage }: Props) {
    const [question, setQuestion] = useState<Question | null>(null)
    const [answer, setAnswer] = useState('')
    const [result, setResult] = useState<Result | null>(null)

    function loadQuestion() {
        fetch(`/api/skills/${skillId}/question`)
            .then((response) => response.json())
            .then((data: Question) => setQuestion(data))
    }
    useEffect(loadQuestion, [skillId])

    function next() {
        setAnswer('')
        setResult(null)
        loadQuestion()
    }

    function check(event: React.FormEvent) {
        event.preventDefault() // stop the browser reloading the page
        if (!question) return
        fetch(`/api/skills/${skillId}/answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: question.question_id, answer }),
        })
            .then((response) => response.json())
            .then((data: Result) => {
                setResult(data)
                onStage(data.stage) // tell App, so the dots and the tree update
            })
    }

    if (!question) return <p>Loading a question...</p>

    return (
        <section className="practice">
            <h2>Practice</h2>
            <form onSubmit={check}>
                <p className="prompt">{question.prompt}</p>
                {question.choices ? (
                    <div className="choices">
                        {question.choices.map((choice) => (
                            <label key={choice}>
                                <input
                                    type="radio"
                                    name="answer"
                                    checked={answer === choice}
                                    onChange={() => setAnswer(choice)}
                                />
                                {choice}
                            </label>
                        ))}
                    </div>
                ) : (
                    <input
                        className="answer-box"
                        aria-label="Your Answer"
                        value={answer}
                        onChange={(event) => setAnswer(event.target.value)}
                    />
                )}
                {!result && (
                    <button type="submit" disabled={answer.trim() === ''}>
                        Check
                    </button>
                )}
            </form>

            {result && (
                <div className={result.correct ? 'feedback correct' : 'feedback not-quite'} role="status">
                    <p className="verdict">{result.correct ? 'Correct!' : 'Not quite.'}</p>
                    {result.explanation && <p>{result.explanation}</p>}
                    <button type="button" onClick={next}>
                        Next Question
                    </button>
                </div>
            )}
        </section>
    )
}

export default Practice
