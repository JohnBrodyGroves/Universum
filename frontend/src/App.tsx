import { useEffect, useState } from 'react'
import Rail from './components/Rail'
import StepProgress from './components/StepProgress'
import Practice from './components/Practice'
import logo from './assets/logo.png'
import Markdown from 'react-markdown'
import SkillTree from './components/SkillTree'

type Skill = {
  id: string
  title: string
  branch: string
  path: string[]
  prerequisites: string[]
}

function App() {
  const [skills, setSkills] = useState<Skill[]>([])
  const [error, setError] = useState('')
  const [lesson, setLesson] = useState('')
  const [screen, setScreen] =useState<'lesson' | 'tree'> ('lesson')

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
  useEffect(() => {
    if (!current) return
    fetch(`/api/skills/${current.id}`)
      .then((response) => {
        if (!response.ok) throw new Error(`Server said ${response.status}`)
        return response.json()
      })
      .then((data: { lesson: string }) => setLesson(data.lesson))
      .catch((err: Error) => setError(err.message))
  }, [current])
  return (
    <div className="app">
      <Rail current={screen} onPick={setScreen} />
      <main>
        {error && <p role="alert">Could not load skills: {error}</p>}
        {screen === 'tree' && <SkillTree skills={skills} />}
        {screen === 'lesson' && (
          <>
            {current && (
              <header className="skill-head">
                <p className="eyebrow">
                  {current.branch} · Skill {skills.indexOf(current) + 1} of {skills.length}
                </p>
                <h1>{current.title}</h1>
              </header>
            )}
            <div className="lesson">
              <Markdown>{lesson}</Markdown>
            </div>
            {current && <Practice skillId={current.id}/>}
          </>
        )}
      </main>
      <aside>
        <img className="logo" src={logo} alt="Universum" />
        {screen === 'lesson' && <StepProgress current={1} done={[0]} />}
      </aside>
    </div>
  )
}

export default App
