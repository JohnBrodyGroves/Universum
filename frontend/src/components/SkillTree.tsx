import { useEffect, useState } from "react"

type Skill = {
    id: string
    title: string
    path: string[]
    prerequisites: string[]
}

// A skill plus what the learner has done with it
type Tile = Skill & {
    stage: number
    needs: string[]
}

type Group = {
    name: string
    tiles: Tile[]
    groups: Group[]
}

// Where a skill sits on the map: which direction, and how far out
type Spot = {
    tile: Tile
    angle: number
    ring: number
}

const LEVELS = ['Learn', 'Practice', 'Check 1', 'Check 2', 'Check 3']
const RING = 130 // Distance between rings
const NODE = 24 // Radius of a skill circle

// Turn each skill's folder path into nested groups, as dep as the folders go
function buildGroups(tiles: Tile[]): Group {
    const root: Group = { name: '', tiles: [], groups: [] }
    for (const tile of tiles) {
        let group = root
        for (const name of tile.path) {
            let child = group.groups.find((g) => g.name === name)
            if (!child) {
                child = { name, tiles: [], groups: [] }
                group.groups.push(child)
            }
            group = child
        }
        group.tiles.push(tile)
    }
    return root
}

function countSkills(group: Group): number {
    return group.tiles.length + group.groups.reduce((sum, g) => sum + countSkills(g), 0)
}

// "whole-number-operations" -> "whole number operations"
function niceName(folder: string) {
    const words = folder.replace(/-/g, '')
    return words[0].toUpperCase() + words.slice(1)
}

// Ring 1 = no prerequisites. Otherwise one ring further out than the furthest prerequisite.
function findRings(skills: Skill[]) {
    const byId = new Map(skills.map((skill) => [skill.id, skill]))
    const rings = new Map<string, number>()
    function ringOf(id: string): number {
        const known = rings.get(id)
        if (known) return known
        const prereqs = byId.get(id)?.prerequisites ?? []
        const ring = 1 + Math.max(0, ...prereqs.map(ringOf))
        rings.set(id, ring)
        return ring
    }
    skills.forEach((skill) => ringOf(skill.id))
    return rings
}

// Give a group a slice of the circle, then share that slice among its skills and subgroups by size
function placeGroup(group: Group, start: number, end: number, rings: Map<string, number>, spots: Spot[]){
    const step = (end - start) / countSkills(group)
    const share = step * group.tiles.length
    // Skills on different rings can line up in the same direction, so a chain of skills runs straight outward
    // Only skills on the same ring need to sit side by side
    for (const tile of group.tiles) {
        const ring = rings.get(tile.id) ?? 1
        const sameRing = group.tiles.filter((t) => rings.get(t.id) === ring)
        const place = sameRing.indexOf(tile)
        spots.push({ tile, angle: start + (share * (place + 0.5)) / sameRing.length, ring })
    }
    let at = start + share
    for (const child of group.groups) {
        const size = step * countSkills(child)
        placeGroup(child, at, at + size, rings, spots)
        at += size
    }
}

function point(angle: number, ring: number) {
    return { x: Math.cos(angle) * ring * RING, y: Math.sin(angle) * ring * RING }
}

function SkillNode({ spot, color }: { spot: Spot; color: string }) {
    const { tile } = spot
    const { x, y } = point(spot.angle, spot.ring)
    const locked = tile.needs.length > 0
    let status = `level ${tile.stage} of ${LEVELS.length}`
    if (locked) status = `locked, needs ${tile.needs.join(', ')}`

    // The circle's outline is cut into 5 pieces, like an XP bar bent into a ring
    const piece = (2 * Math.PI * NODE) / LEVELS.length
    const earned = Array(tile.stage).fill(`${piece - 4} 4`).join(' ') + ` 0 ${2 * Math.PI * NODE}`

    return (
        <g className={locked ? 'node locked' : 'node'} transform={`translate(${x} ${y})`} role="img" aria-label={`${tile.title}: ${status}`}>
            <title>{`${tile.title}: ${status}`}</title>
            <circle r={NODE} className="node-base" strokeDasharray={`${piece - 4} 4`} transform="rotate(-90)" />
            <circle r={NODE} className="node-earned" stroke={color} strokeDasharray={earned} transform="rotate(-90)" />
            <text y={NODE + 18} className="node-label">{tile.title}</text>
        </g>        
    )
}

function SkillTree({ skills }: { skills: Skill[] }) {
    const [progress, setProgress] = useState<Record<string, number>>({})
    const [error, setError] = useState('')

    useEffect(() => {
        fetch('/api/progress')
            .then((response) => {
                if (!response.ok) throw new Error(`Server said ${response.status}`)
                return response.json()
            })
            .then((data: Record<string, number>) => setProgress(data))
            .catch((err: Error) => setError(err.message))
    }, [])
    const titles = Object.fromEntries(skills.map((skill) => [skill.id, skill.title]))

    const tiles = skills.map((skill) => ({
        ...skill,
        stage: progress[skill.id] ?? 0,
        // A skill stays locked until every prerequisite is mastered
        needs: skill.prerequisites
            .filter((id) => (progress[id] ?? 0) < LEVELS.length)
            .map((id) => titles[id]),
    }))
    if (tiles.length === 0) return null

    const root = buildGroups(tiles)
    const spots: Spot[] = []
    placeGroup(root, -Math.PI / 2, 1.5 * Math.PI, findRings(skills), spots)
    const spotOf = new Map(spots.map((spot) => [spot.tile.id, spot]))

    // Each top-level subject gets its own colour, spread evenly around the colour wheel
    const branches = root.groups.map((group) => group.name)
    const colorOf = (tile: Tile) => `hsl(${(branches.indexOf(tile.path[0]) * 360) / branches.length} 60% 42%)`

    const outer = Math.max(...spots.map((spot) => spot.ring)) + 1
    const size = (outer + 0.8) * RING

    return (
        <section className="tree">
            <h1>Skill tree</h1>
            {error && <p role="alert">Could not load your progress: {error}</p>}
            <svg className="map" viewBox={`${-size} ${-size} ${size * 2} ${size * 2}`}>
                {Array.from({ length: outer - 1 }, (_, i) => (
                    <circle key={i} r={(i + 1) * RING} className="ring" />
                ))}

                {spots.map((spot) => {
                    const to = point(spot.angle, spot.ring)
                    const from = spot.tile.prerequisites.map((id) => spotOf.get(id)!)
                    const starts = from.length ? from.map((s) => point(s.angle, s.ring)) : [{ x: 0, y: 0 }]
                    return starts.map((start, i) => (
                        <line key={`${spot.tile.id}-${i}`} x1={start.x} y1={start.y} x2={to.x} y2={to.y} className="path" />
                    ))
                })}

                {root.groups.map((group) => {
                    const mine = spots.filter((spot) => spot.tile.path[0] === group.name)
                    const angles = mine.map((spot) => spot.angle)
                    const angle = (Math.min(...angles) + Math.max(...angles)) / 2
                    const { x, y } = point(angle, outer)
                    return (
                        <text key={group.name} x={x} y={y} className="branch-label" fill={colorOf(mine[0].tile)}>
                            {niceName(group.name)}
                        </text>
                    )
                })}

                <circle r={NODE * 1.8} className="center" />
                <text className="center-label" dy="0.35em">You</text>

                {spots.map((spot) => <SkillNode key={spot.tile.id} spot={spot} color={colorOf(spot.tile)} />)}
            </svg>
        </section>
    )
}

export default SkillTree