import React from "react" 
import PageTemplate from "@components/reusable/template/PageTemplate.tsx";
import st from "../../styles/product_pg/App.module.css"
import { useRouter } from 'next/router'
import config from "../../config";
import { useSelector } from "react-redux";
import {useEffect} from "react"
import Header from "./components/header";
import Request_Btn from "./components/request_btn";
import MainContent from "./components/main-content";
import axios from 'axios' 


// 
// {                                                        {
//    about_us : "", 
//    company_name : "", 
//    contractor_name : "", 
//    phone_no : "", 
//    website : "", 
//    address : ""
//   }

// contractor_id": "vycs78",
  // //   "name": "proVis",
  // //   "email": "7provis7@gmail.com",
  // //   "address": "Sweet Home Alabama",
  // //   "phone_no": 9205231951,
  // //   "company_id": "vycs78"

// let query_obj = {company_img_url : data.company_img_url , 
//   product_img_url : data.product_img_url,
//   description : data.description , 
//   contractor_id  : data.contractor_id,
//   company_id : data.company_id , 
//   category : data.category , 
//   id  : data.p_uid}  


function App() {
  let router = useRouter() 
  // let url1 =
  //   "https://img.staticmb.com/mbcontent//images/uploads/2022/12/Most-Beautiful-House-in-the-World.jpg";
  // let url2 =
  //   "https://s3.amazonaws.com/cdn.designcrowd.com/blog/100-Famous-Brand%20Logos-From-The-Most-Valuable-Companies-of-2020/apple-logo.png";

  


  let slug = router.query  
  let url1 = slug.product_img_url 
  let url2 = slug.company_img_url 
  
  console.log(slug) 
  
  const jwt = useSelector((state) => state.storage.jwt);

  const { apiUrl } = config;

  let [contractorState, SetcontractorState] = React.useState({
   contractor_name : "", 
   phone_no : "", 
   address : ""
  })

  let [companyState, SetcompanyState] = React.useState({
    company_name : "", 
    website : "",
    about_us : ""
   })
  


  // useEffect( () => {
  //   Promise.all([
  //     fetch(`${apiUrl}/api/contractors/${slug.contractor_id}`, {
  //       method : 'GET', 
  //       headers: {
  //         "Content-Type": "application/json" 
  //           // Authorization: `Bearer ${jwt}`,
  //       },
  //     }),
      
  //     fetch(`${apiUrl}/api/companies/${slug.company_id}`, {
  //       method : 'GET', 
  //       headers: {
  //         "Content-Type": "application/json" 
  //           // Authorization: `Bearer ${jwt}`,
  //       },
  //     })
      
  //   ])
  //   .then(([contractor_res,company_res]) => Promise.all([contractor_res.json(), company_res.json()])
  //   .then(
  //     ([contractor_data, company_data]) =>{ 
    //     SetcontractorState((prevState) => {
    //       return { ...prevState, 
    //         contractor_name : contractor_data.name, 
    //         phone_no : contractor_data.phone_no,
    //         address : contractor_data.address
    //     }
    //   }) 
    //   ; 
    //   SetcompanyState((prevState) => {
    //     return { ...prevState, 
    //       company_name : company_data.name, 
    //       website :  company_data.website_link,
    //       about_us :  company_data.about_us
    //   }
    // })
  //   })
  //   ).catch((err) => console.error(err));
  // }, []) 

   useEffect( () => {
    const fetchData = async () => {
      const contractor_response  = await axios(`${apiUrl}/api/contractors/${slug.company_id}`) ; 
      const company_response = await axios(`${apiUrl}/api/companies/${slug.company_id}`) ; 
      const contractor_data = contractor_response.data ; 
      const company_data = company_response.data ; 
      console.log("logging ...") 
      console.log(contractor_data) ; console.log(company_data) ; 
            SetcontractorState((prevState) => {
              return { ...prevState, 
                contractor_name : contractor_data.name, 
                phone_no : contractor_data.phone_no,
                address : contractor_data.address
            }
          }) ; 
            SetcompanyState((prevState) => {
              return { ...prevState, 
                company_name : company_data.name, 
                website :  company_data.website_link,
                about_us :  company_data.about_us
            }
          })
    } ; 

    fetchData() ;
  }
   , []
    )
  


//  useEffect( () => {
//     fetch(`${apiUrl}/api/companies/${slug.company_id}`, {
//       method : 'GET', 
//       headers: {
//         "Content-Type": "application/json" 
//           // Authorization: `Bearer ${jwt}`,
//       },
//     }).then((response) => response.json().then(
//       (data) => 
//         SetcompanyState((prevState) => {
//           return { ...prevState, 
//             company_name : data.name, 
//             website : data.website_link,
//             about_us : data.about_us
//         }
//       })
//     )).catch((err) => console.error(err));
//   }, [companyState]) 
  




  // function genobj(data){
  //   let about_us = data.about_us 
  //   let business_details = { name : slug.contractor_name, address : data.business.address, website : data.business.website_link}
  //   let project_data = data.projects.map((x) => { return {name : x.project_name, img : x.project_img_url} } )
  //   return {about_us, business_details, projects : project_data} 
  // }
  // let business_details = {
  //   name: "Aaveg",
  //   address: "B250, MG Road, New Manglapuri Mehrauli- Gurgaon Road South Delhi",
  //   phone_number: 9205231951,
  //   website: "www.treac.in",
  // };

  // let obj = {
  //   about_us:
  //     "TR Engineer and Contractor. Construction and renovation services. Www.trengineer.com",
  //   projects: project_data,
  //   business_details: business_details,
  // };

  return (
    <PageTemplate transparentNav={false} outsideApp darkBg={true} noFilter>
    <div>
      
      <div className={st.container}>
        <Header
          header_image_url={url1}
          company_img_url={url2}
          contractor= {slug.contractor_name} 
          category= {slug.category}
          className={st.header}
        />
        <div className={st.sticky}>
          <Request_Btn
            btn_text="Make a Request"
            modal_header="Make a Request"
            modal_description="Send a message to this pro to meet them"
            label="Message: "
            modal_btn_text="Send"
            className={st.request_btn}
            p_uid = {slug.id} 
          />
        </div>

        <MainContent company_obj={companyState} contractor_obj = {contractorState} className={st.main_content} />
      </div>
    </div>
  </PageTemplate>
  );



}

export default App;
