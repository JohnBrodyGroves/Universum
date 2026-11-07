const STEPS = [
    { name: 'Learn', short: 'L' },
    { name: 'Practice', short: 'P' },
    { name: 'Check 1', short: '1' },
    { name: 'Check 2', short: '2' },
    { name: 'Check 3', short: '3' },
]

type Props = { current: number; done: number[] }

function StepProgress({ current, done }: Props) {
    return (
        <ol className="steps" aria-label="Progress in this skill">
            {STEPS.map((step, i) => {
                let state = 'locked'
                if (done.includes(i)) state = 'done'
                else if (i === current) state = 'current'

                return (
                    <li key={step.name} className={state}>
                        <span className="dot" aria-label={`${step.name}: ${state}`}>{step.short}</span>
                        <span className="step-name">{step.name}</span>
                    </li>


                )
            })}
        </ol>
    )
}

export default StepProgress
