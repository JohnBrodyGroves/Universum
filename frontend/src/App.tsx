import { useEffect, useState } from 'react'
import Rail from './components/Rail'

type Skill = {
  id: string
  title: string
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

  return (
    <div className="app">
      <Rail current="lesson" />
      <main>
        <h1>Universum</h1>
        <h2>Math skills</h2>
        {error && <p role="alert">Could not load skills: {error}</p>}
        <ul>
          {skills.map((skill) => (
            <li key={skill.id}>{skill.title}</li>
          ))}
        </ul>
      </main>
      <aside></aside>
    </div>
  )
}

export default App
