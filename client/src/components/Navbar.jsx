import {Link} from "react-router-dom";


function Navbar(){


return(

<nav className="
flex 
justify-between
items-center
px-10
py-5
bg-slate-900
">


<h1 className="
text-2xl
font-bold
text-blue-400
">

SignatureGuard AI

</h1>


<div className="space-x-6">


<Link to="/">
Home
</Link>


<Link to="/login">
Login
</Link>


<Link to="/register">

Register

</Link>


</div>


</nav>


)

}


export default Navbar;