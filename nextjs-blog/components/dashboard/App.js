import React, { useEffect } from "react" 
import { useSelector } from "react-redux";
import { RootState } from "../../redux/reducers"
import config from "../../config";
import Order from "./components/order"
import PageTemplate from "@components/reusable/template/PageTemplate";
import st from "../../styles/dashboard/app.module.css" 
import { Card, Space } from 'antd';
import axios from 'axios' 

export default function App(){
    let obj  = {
        company_img_url : "", 
        product_img_url : "", description : "", company_name : "", location : "", category : "", order_date_time : "",
        company_id :"", p_uid : "", message : ""
    }


    const id = useSelector((state) => state.storage.userID)
    // get user id from state
    let [userState, setUserState] = React.useState({name : "", emailid: "", phone_number : ""})

    let [orderState, setOrderState] = React.useState([]) 

    function genarr(data){
        return data.map((x) => <Order obj = {x} /> ) 
    }

    const { apiUrl } = config;



    useEffect(() =>{
        const fetchData = async ()=>{
            const customer_response   = await axios(`${apiUrl}/api/customers/${id}`) ;
            const order_response = await axios(`${apiUrl}/api/customers/${id}/orders`); 
            const customer_data = customer_response.data 
            const order_data = order_response.data 
            
            setUserState({name : customer_data.name, emailid : customer_data.emailid, phone_number: customer_data.phone_number});
            setOrderState(genarr(order_data));
           
        };
       
        fetchData() 
    } , []) ; 

   
      



    let dashboard_url = "https://img.freepik.com/free-photo/brown-wooden-flooring_53876-90802.jpg?w=996&t=st=1680938897~exp=1680939497~hmac=d5bfaf1218dcd7b4c1c96e2696088de57dc236aa8f4fb73e46df65a56e51fda8" 
    return (
        <PageTemplate transparentNav={false} outsideApp darkBg={true} noFilter>
            <div className= {st.header}>
                    <img src = {dashboard_url} className={st.dashboard_img} />
           </div>
        <div className={st.detailscontainer}>
                <Space direction="vertical" size={16} className={st.space}>
                    
                    <Card title="User Dashboard"  style={{ width: 400 , height : 200}} className={st.card}>
                    
                    <p><strong>Name: </strong> <span className={st.label}>{userState.name}</span> </p>
                    <p><strong>Phone Number: </strong><span className={st.label}>9415468459</span> </p>
                    <p><strong>Email Address: </strong><span className={st.label}> {userState.emailid} </span></p>

       

                    </Card>

                 
                </Space>
            <div className={st.orderdetails} >
                <div className={st.ordertext}>Your Orders</div>
                {orderState.length==0?"You have no current orders!":orderState} 
            </div>
        </div>
    </PageTemplate>
    )

}



