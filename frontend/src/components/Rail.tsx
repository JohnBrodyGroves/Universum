type Props = { 
    current: 'profile' | 'home' | 'lesson' | 'tree' | 'settings'
    onPick: (screen: 'lesson' | 'tree') => void
 }

function Rail({ current, onPick }: Props) {
    const mark = (name: Props['current']) => (current === name ? 'page' : undefined)

    return (
        <nav className="rail" aria-label="Main Menu">
            <button type="button" aria-label="Profile" aria-current={mark('profile')}>
                <svg viewBox="0 0 32 32"><circle cx="16" cy="11" r="6" /><path d="M5 28c1.5-6 6-9 11-9s9.5 3 11 9z" /></svg>
            </button>
            <button type="button" aria-label="Home" aria-current={mark('home')}>
                <svg viewBox="0 0 32 32"><path d="M4 15 16 4l12 11" /><path d="M8 13v14h6v-8h4v8h6V13" /></svg>
            </button>
            <button type="button" aria-label="Current Lesson" aria-current={mark('lesson')} onClick={() => onPick('lesson')}>
                <svg viewBox="0 0 32 32"><path d="M16 9c-3-2.5-7-3-12-2.5v18c5-.5 9 0 12 2.5 3-2.5 7-3 12-2.5v-18c-5-.5-9 0-12 2.5z" /><path d="M16 9v18" /></svg>
            </button>
            <button type="button" aria-label="Skill Tree" aria-current={mark('tree')} onClick={() => onPick('tree')}>
                <svg viewBox="0 0 32 32"><path d="M16 29V17m0 4-4-3m4 1 3-3" /><path d="M10 22c-4 0-6-3-5-6-2-2-1-6 2-7 0-4 5-6 8-4 3-3 9-1 9 3 3 1 4 5 2 7 1 4-2 7-6 7z" /><path d="M11 29h10" /></svg>
            </button>
            <button type="button" className="rail-bottom" aria-label="Settings" aria-current={mark('settings')}>
                <svg viewBox="0 0 32 32"><path d="M25.7 13.6 29.3 14 29.3 18 25.7 18.4 24.5 21.2 26.9 24 24 26.9 21.2 24.5 18.4 25.7 18 29.3 14 29.3 13.6 25.7 10.8 24.5 8 26.9 5.1 24 7.5 21.2 6.3 18.4 2.7 18 2.7 14 6.3 13.6 7.5 10.8 5.1 8 8 5.1 10.8 7.5 13.6 6.3 14 2.7 18 2.7 18.4 6.3 21.2 7.5 24 5.1 26.9 8 24.5 10.8z" /><circle cx="16" cy="16" r="4.5" /></svg>
            </button>
        </nav>
    )
}

export default Rail
