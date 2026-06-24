import { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";

function Dashboard() {

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);


  const handleFileChange = (e) => {

    const selectedFile = e.target.files[0];

    if (!selectedFile) {
      return;
    }


    setFile(selectedFile);


    setPreview(
      URL.createObjectURL(selectedFile)
    );


    setPrediction(null);

  };



  const handleUpload = async () => {


    if (!file) {

      toast.error(
        "Please select a signature image"
      );

      return;

    }



    try {


      setLoading(true);



      const formData = new FormData();


      formData.append(
        "image",
        file
      );



      const response = await axios.post(

     "https://signatureguard-ai-5.onrender.com/predict",

        formData,

        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }

      );



      console.log(
        "API Response:",
        response.data
      );



      setPrediction(
        response.data
      );



      toast.success(
        "Verification completed"
      );



    } catch (error) {


      console.error(
        "Upload Error:",
        error
      );


      toast.error(
        "Verification Failed"
      );


    } finally {


      setLoading(false);


    }

  };




  return (

    <div className="min-h-screen bg-slate-950 text-white p-8">


      <div className="max-w-6xl mx-auto">



        <h1 className="text-4xl font-bold text-center mb-3">

          SignatureGuard AI

        </h1>



        <p className="text-center text-gray-400 mb-10">

          AI Powered Signature Forgery Detection System

        </p>




        <div className="grid md:grid-cols-2 gap-8">





          <div className="bg-slate-900 rounded-2xl p-6">



            <h2 className="text-2xl font-semibold mb-5">

              Upload Signature

            </h2>




            {

              preview ?


              <img

                src={preview}

                alt="signature preview"

                className="w-full h-72 object-contain bg-slate-800 rounded-xl"

              />


              :


              <div className="h-72 bg-slate-800 rounded-xl flex items-center justify-center">

                No Signature Selected

              </div>


            }





            <input

              type="file"

              accept="image/*"

              onChange={handleFileChange}

              className="w-full mt-5"

            />





            <button

              onClick={handleUpload}

              disabled={loading}

              className="w-full mt-5 bg-blue-600 hover:bg-blue-700 py-3 rounded-xl font-semibold"

            >


              {

                loading

                ?

                "Verifying..."

                :

                "Start Verification"


              }


            </button>



          </div>







          <div className="bg-slate-900 rounded-2xl p-6">



            <h2 className="text-2xl font-semibold mb-5">

              Verification Result

            </h2>





            {

              prediction ?


              <div className="space-y-4">


                <p>

                  <span className="font-bold">
                    Status:
                  </span>{" "}

                  {prediction.status}

                </p>




                <p>

                  <span className="font-bold">
                    Confidence:
                  </span>{" "}

                  {prediction.confidence}%

                </p>




                <p>

                  <span className="font-bold">
                    Image:
                  </span>{" "}

                  {prediction.image}

                </p>



              </div>


              :


              <p>
                No prediction available
              </p>


            }




          </div>




        </div>




      </div>



    </div>

  );

}


export default Dashboard;