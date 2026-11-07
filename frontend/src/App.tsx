import { useEffect, useState } from 'react'
import Rail from './components/Rail'
import StepProgress from './components/StepProgress'
import logo from './assets/logo.png'

type Skill = {
  id: string
  title: string
  branch: string
  prerequisites: string[]
}

function App() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/skills')
      .then((response) => {
        if (!response.ok) throw new Error(`Server said ${response.status}`)
        return response.json()
      })
      .then((data: Skill[]) => setSkills(data))
      .catch((err: Error) => setError(err.message))
  }, [])
  const current = skills.find((skill) => skill.prerequisites.length === 0)
  return (
    <div className="app">
      <Rail current="lesson" />
      <main>
        {error && <p role="alert">Could not load skills: {error}</p>}
        {current && (
          <header className="skill-head">
            <p className="eyebrow">
              {current.branch} · Skill {skills.indexOf(current) + 1} of {skills.length}
            </p>
            <h1>{current.title}</h1>
          </header>
        )}
      </main>
      <aside>
        <img className="logo" src={logo} alt="Universum" />
        <StepProgress current={1} done={[0]} />
      </aside>
    </div>
  )
}

export default App
