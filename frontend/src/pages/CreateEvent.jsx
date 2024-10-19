import CreateEventForm from "../components/CreateEventForm";
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';

function CreateEvent() {
    return(
        <div className="flex flex-col min-h-screen">
  <div className="flex flex-1">
    <Sidebar />
    <main className="flex-1">
      <div className="bg-white min-h-screen p-6">
        <CreateEventForm />
      </div>
    </main>
  </div>
  <Footer />
</div>
)};
export default CreateEvent;