interface ProjectCardProps {
  project: {
    title: string
    summary: string
    track: string
    repo_url: string
  }
}

const Projectcard = (props: ProjectCardProps) => {
  return (
    <div className="rounded-2xl border border-white/10 p-6 text-white shadow-lg backdrop-blur-lg">
      <div className='space-y-4'>
      <div className='font-bold text-purple-100'>{props.project.title}</div>
      <div className='font-mono text-gray-300'>{props.project.summary}</div>
      <div className='font-semibold text-purple-600'>{props.project.track}</div>
      <a href={props.project.repo_url} className='inline-block rounded-xl bg-linear-to-br from-[#0f3388] to-[#4d1bcc] backdrop-blur-md border border-gray-400 px-5 py-3 hover:from-[#648dee] hover:via-[#2a55f0] hover:to-[#4215b3] transition'>View Repository</a>
      </div>
    </div>
  )
}

export default Projectcard