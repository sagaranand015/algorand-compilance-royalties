import { useState } from 'react';
import Layout from '../components/layout'
import HttpClient from "react-http-client";
import { authToken } from '../components/complianceTypes';

const Regulator = () => {

    const [emissionType, setEmissionType] = useState("")
    const [emissionDescription, setEmissionDescription] = useState("")
    const [maxEmissions, setMaxEmissions] = useState("")
    

    const changeEmissionType = (e) => {
        setEmissionType(e.target.value)
    }

    const changeEmissionDescription = (e) => {
        setEmissionDescription(e.target.value)
    }

    const changeMaxEmissions = (e) => {
        setMaxEmissions(e.target.value)
    }

    const handleControlCreate = async () => {
        if (emissionType && emissionDescription && maxEmissions) {
            console.log(emissionType+" "+emissionDescription+" "+maxEmissions)
            try {
                const createControlResponse = await HttpClient.post("http://localhost:8080/regulator/control", {
                    // body: {
                        "emission_param": String(emissionType),
                        "emission_desc": String(emissionDescription),
                        "emission_max": String(maxEmissions)
                    // }
                }, {
                    'Authorization': authToken
                });
                if (!createControlResponse.status) {
                    console.log("Unable to Create Control");
                }
                else {
                    console.log(createControlResponse)
                    alert("Control Created Succesfully")
                }
            } catch (e) {
                console.log("Create Control FAILED", e);
            }
        }
        else {
            alert("Please enter all values")
        }
    }


    return (
        <Layout>
            Create Emission Control
            <input className="block mt-4 bg-gray-100 px-4 py-2 w-[25%]" type="text" name="Emission Type" placeholder="Emission Type" value={emissionType} onChange={changeEmissionType} />
            <input className="block mt-4 bg-gray-100 px-4 py-2 w-[25%]" type="text" name="Description" placeholder="Description" value={emissionDescription} onChange={changeEmissionDescription} />
            <input className="block mt-4 bg-gray-100 px-4 py-2 w-[25%]" type="text" name="Max Emissions" placeholder="Max Emissions" value={maxEmissions} onChange={changeMaxEmissions} />
            <button className="block bg-orange-400 px-4 py-2 mt-4" onClick={handleControlCreate}>Create</button>
        </Layout>
    )
}

export default Regulator