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
  const [progress, setProgress] = useState<Record<string, number>>({})
  const [openId, setOpenId] = useState('')
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
  useEffect(() => {
    fetch('/api/progress')
      .then((response) => {
        if (!response.ok) throw new Error(`Server said ${response.status}`)
        return response.json()
      })
      .then((data: Record<string, number>) => setProgress(data))
      .catch((err: Error) => setError(err.message))
  }, [])
  // The skill picked on the tree, or the first starting skill until one is picked
  const current = skills.find((skill) => skill.id === openId) ?? skills.find((skill) => skill.prerequisites.length === 0)
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
  const stage = current ? progress[current.id] ?? 0 : 0
  return (
    <div className="app">
      <Rail current={screen} onPick={setScreen} />
      <main>
        {error && <p role="alert">Could not load skills: {error}</p>}
        {screen === 'tree' && (
          <SkillTree
            skills={skills}
            progress={progress}
            onOpen={(id) => {
              setOpenId(id)
              setScreen('lesson')
            }}
          />
        )}
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
            {current && (
              <Practice
                key={current.id}
                skillId={current.id}
                onStage={(stage) => setProgress((old) => ({ ...old, [current.id]: stage }))}
              />
            )}
          </>
        )}
      </main>
      <aside>
        <img className="logo" src={logo} alt="Universum" />
        {screen === 'lesson' && <StepProgress current={stage} done={Array.from({ length: stage }, (_, i) => i)} />}
      </aside>
    </div>
  )
}

export default App
