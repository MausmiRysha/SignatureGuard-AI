import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Navbar */}
      <nav className="flex justify-between items-center px-12 py-6 bg-slate-900">
        <h1 className="text-3xl font-bold text-blue-400">
          SignatureGuard AI
        </h1>

        <div className="space-x-8">
          <Link to="/" className="hover:text-blue-400">
            Home
          </Link>

          <Link to="/login" className="hover:text-blue-400">
            Login
          </Link>

          <Link to="/register" className="hover:text-blue-400">
            Register
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center h-[80vh] text-center px-6">
        <h1 className="text-6xl font-bold mb-6">
          Detect Signature Forgery Using AI
        </h1>

        <p className="text-2xl text-gray-300 mb-10">
          Deep learning powered signature verification with CNN technology
        </p>

        <Link
          to="/dashboard"
          className="bg-blue-600 hover:bg-blue-700 px-10 py-4 rounded-xl text-xl font-semibold"
        >
          Start Verification
        </Link>
      </div>
    </div>
  );
}

export default Home;