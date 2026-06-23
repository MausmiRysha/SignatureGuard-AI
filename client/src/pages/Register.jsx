import { useState } from "react";
import { Link } from "react-router-dom";
import { User, Mail, Lock } from "lucide-react";
import { motion } from "framer-motion";


function Register() {

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: ""
  });


  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  };


  const handleSubmit = (e) => {

    e.preventDefault();

    console.log(formData);

    // Backend API connection will come in Phase 2

  };


  return (

    <div className="
      min-h-screen
      flex
      items-center
      justify-center
      bg-slate-950
      px-5
    ">


      <motion.div

        initial={{opacity:0, y:40}}

        animate={{opacity:1, y:0}}

        className="
          w-full
          max-w-md
          bg-slate-900
          p-8
          rounded-2xl
          shadow-xl
        "

      >


        <h1 className="
          text-3xl
          font-bold
          text-center
          text-blue-400
          mb-3
        ">

          Create Account

        </h1>


        <p className="
          text-gray-400
          text-center
          mb-8
        ">

          Join SignatureGuard AI

        </p>



        <form onSubmit={handleSubmit}>


          {/* Name */}

          <div className="
            flex
            items-center
            bg-slate-800
            rounded-lg
            mb-4
            px-4
          ">

            <User size={20}/>


            <input

              type="text"

              name="name"

              placeholder="Full Name"

              value={formData.name}

              onChange={handleChange}

              className="
                w-full
                bg-transparent
                p-3
                outline-none
              "

              required

            />

          </div>




          {/* Email */}

          <div className="
            flex
            items-center
            bg-slate-800
            rounded-lg
            mb-4
            px-4
          ">

            <Mail size={20}/>


            <input

              type="email"

              name="email"

              placeholder="Email Address"

              value={formData.email}

              onChange={handleChange}

              className="
                w-full
                bg-transparent
                p-3
                outline-none
              "

              required

            />

          </div>





          {/* Password */}

          <div className="
            flex
            items-center
            bg-slate-800
            rounded-lg
            mb-6
            px-4
          ">


            <Lock size={20}/>


            <input

              type="password"

              name="password"

              placeholder="Password"

              value={formData.password}

              onChange={handleChange}

              className="
                w-full
                bg-transparent
                p-3
                outline-none
              "

              required

            />


          </div>





          <button

            type="submit"

            className="
              w-full
              bg-blue-600
              hover:bg-blue-700
              transition
              py-3
              rounded-xl
              font-semibold
              text-lg
            "

          >

            Register

          </button>



        </form>





        <p className="
          text-center
          text-gray-400
          mt-6
        ">


          Already have an account?


          <Link

            to="/login"

            className="
              text-blue-400
              ml-2
            "

          >

            Login

          </Link>


        </p>



      </motion.div>


    </div>

  );

}


export default Register;