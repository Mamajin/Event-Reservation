import { Link } from 'react-router-dom';

export default function Footer() {
    return (
        <footer className="footer bg-neutral text-neutral-content p-10">
            <nav className="pl-80">
                <h6 className="footer-title">Services</h6>
                <Link to="/services/branding" className="link link-hover">Branding</Link>
                <Link to="/services/design" className="link link-hover">Design</Link>
                <Link to="/services/marketing" className="link link-hover">Marketing</Link>
                <Link to="/services/advertisement" className="link link-hover">Advertisement</Link>
            </nav>
            <nav className="pl-4">
                <h6 className="footer-title">Team</h6>
                <Link to="/team/about-us" className="link link-hover">About us</Link>
                <Link to="/team/contact" className="link link-hover">Contact</Link>
                <Link to="/team/jobs" className="link link-hover">Jobs</Link>
                <Link to="/team/press-kit" className="link link-hover">Press kit</Link>
            </nav>
            <nav className="pl-4">
                <h6 className="footer-title">Legal</h6>
                <Link to="/legal/terms-of-use" className="link link-hover">Terms of use</Link>
                <Link to="/legal/privacy-policy" className="link link-hover">Privacy policy</Link>
                <Link to="/legal/cookie-policy" className="link link-hover">Cookie policy</Link>
            </nav>
        </footer>
    );
}