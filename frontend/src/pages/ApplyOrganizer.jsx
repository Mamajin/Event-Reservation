import OrganizerForm from '../components/OrganizerForm';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';

function ApplyOrganizer() {
    return(
        <div className="flex flex-col min-h-screen">
  <div className="flex flex-1">
    <Sidebar />
    <main className="flex-1">
      <div className="bg-white min-h-screen p-6">
        <OrganizerForm />
      </div>
    </main>
  </div>
  <Footer />
</div>
)};
export default ApplyOrganizer;