import projects from '../data/fixtures.json'
import Projectcard from '../components/Projectcard'

const Gallery = () => {
  return (
    <>
  <div className="grid grid-cols-1 bg-linear-to-br from-[#070B14] via-[#101A3D] to-[#17093a] md:grid-cols-2 lg:grid-cols-3 gap-4 p-8">

    {projects.projects.map((project) => (
      <Projectcard
        key={project.id}
        project={project}
      />
    ))}

  </div>
  </>
)
}

export default Gallery