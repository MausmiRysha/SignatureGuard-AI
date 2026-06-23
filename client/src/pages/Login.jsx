function Login() {
  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950">

      <div className="w-full max-w-md bg-slate-900/80 backdrop-blur-md p-10 rounded-3xl shadow-2xl border border-slate-700">

        <h1 className="text-4xl font-bold text-center text-white mb-2">
          Welcome Back
        </h1>

        <p className="text-center text-gray-400 mb-8">
          Login to SignatureGuard AI
        </p>

        <input
          type="email"
          placeholder="Enter Email"
          className="
          w-full
          mb-4
          p-4
          rounded-xl
          bg-slate-800
          text-white
          border
          border-slate-600
          focus:outline-none
          focus:border-blue-500
          "
        />

        <input
          type="password"
          placeholder="Enter Password"
          className="
          w-full
          mb-6
          p-4
          rounded-xl
          bg-slate-800
          text-white
          border
          border-slate-600
          focus:outline-none
          focus:border-blue-500
          "
        />

        <button
          className="
          w-full
          py-4
          rounded-xl
          font-semibold
          text-white
          bg-gradient-to-r
          from-blue-500
          to-cyan-500
          hover:from-blue-600
          hover:to-cyan-600
          transition
          duration-300
          "
        >
          Login
        </button>

        <p className="text-center text-gray-400 mt-6">
          Don't have an account?{" "}
          <span className="text-blue-400 cursor-pointer hover:underline">
            Register
          </span>
        </p>

      </div>

    </div>
  );
}

export default Login;