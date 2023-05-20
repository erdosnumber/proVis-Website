import React, { useState, useEffect, Component } from "react";
import axios from "axios" 

import Dropdown from "react-dropdown";
import "react-dropdown/style.css";
import Spinner from "../loader"
import "react-js-dropdavn/dist/index.css";
import { useRouter } from "next/router";
import config from "../../config";
import PageTemplate from "@components/reusable/template/PageTemplate.tsx";
import Listing_Box from "./components/listing_box";
import Card from "./components/card";
import products from "./data/products";
// import Dropdown from "./components/dropdown";
import st from "../../styles/listing_pg/app.module.css";
// import cross from "../../public/listing_pg/cross.png"
// {
//   "p_uid": "vycs78",
//   "location": "Delhi",
//   "category": "interior design",
//   "product_img_url": "https://www.youtube.com/",
//   "product_description": "this is the worst",
//   "company_name": "proVis",
//   "company_img_url": "https://www.youtube.com/",
//   "contractor_id": "82390kf"
// }

function App() {
  let router = useRouter();
  // let card_array = products.map((obj) => <Card obj = {obj} key = {obj.id} />)
  // let arr = ["aaveg","arnav"]

  // let [newLocation,setLocationState] = React.useState("Delhi")
  // let [newCategory,setCategoryState] = React.useState("Interior Designers & Decorators")

  let [newState, SetState] = React.useState({ location: "", category: "" });
  let [cardsState, setCardsState] = React.useState([]);
  let [loader,setLoader]=React.useState(true);

  let cross = "/listing_pg/cross.png";

  let { apiUrl } = config;

  // function gen_obj(data) {
  //   let id = data.p_uid;
  //   let location = data.location;
  //   let category = data.category;
  //   let product_img_url = data.product_img_url;
  //   let description = data.product_description;
  //   let company_name = data.company_name;
  //   let company_img_url = data.company_img_url;
  //   let contractor_id = data.contractor_id;
  //   let contractor_name = data.contractor_name;

  //   let obj = {
  //     id,
  //     location,
  //     category,
  //     product_img_url,
  //     description,
  //     company_name,
  //     company_img_url,
  //     contractor_id,
  //     contractor_name,
  //   };
  //   return obj;
  // }
  // let new_cards = products.map((obj) => (
  //   <Card
  //     clicker={() => router.push({ pathname: "/product_pg", query: query_obj })}
  //     obj={gen_obj(obj)}
  //     key={obj.p_uid}
  //   />
  // ));

  function locationHandler(location) {
    SetState((prevState) => {
      return { ...prevState, location: location.value };
    });
  }

  function categoryHandler(category) {
    SetState((prevState) => {
      return { ...prevState, category: category.value };
    });
  }

  function remove_category() {
    SetState((prevState) => {
      return { ...prevState, category: "" };
    });
  }

  function remove_location() {
    SetState((prevState) => {
      return { ...prevState, location: "" };
    });
  }
  let new_card_array = [];
  // useEffect(() => {
  //   console.log("product fetch");
  //   let url_fetch = `${apiUrl}/api/products/findByTags`;
  //   let loc_fetch = `?location=${newState.location}`;
  //   let cat_fetch = `&category=${newState.category}`;

  //   if (newState.location == "") {
  //     loc_fetch = "";
  //     cat_fetch = "?" + cat_fetch;
  //   }

  //   if (newState.category == "") {
  //     cat_fetch = "";
  //   }
  //   url_fetch = url_fetch + loc_fetch + cat_fetch;

  //   fetch(url_fetch, {
  //     method: "GET",
  //     headers: {
  //       "Content-Type": "application/json",
  //       // Authorization: `Bearer ${jwt}`,
  //     },
  //   })
  //     .then((response) =>
  //       response.json().then((data) => {
  //         console.log("printing data");
  //         console.log(data);
  //         console.log("entered json method");
  //         function gen_obj(data) {
  //           let id = data.p_uid;
  //           let location = data.location;
  //           let category = data.category;
  //           let product_img_url = data.product_img_url;
  //           let description = data.product_description;
  //           let company_name = data.company_name;
  //           let company_img_url = data.company_img_url;
  //           let contractor_id = data.contractor_id;
  //           let contractor_name = data.contractor_name;

  //           let obj = {
  //             id,
  //             location,
  //             category,
  //             product_img_url,
  //             description,
  //             company_name,
  //             company_img_url,
  //             contractor_id,
  //             contractor_name,
  //           };
  //           return obj;
  //         }

  //         function gen_query(data_arr) {
  //           return data_arr.map((x) => ({
  //             company_img_url: x.company_img_url,
  //             product_img_url: x.product_img_url,
  //             description: x.description,
  //             contractor_name: x.contractor_name,
  //             category: x.category,
  //             id: x.p_uid,
  //             company_id: x.company_id,
  //             contractor_id: x.contractor_id,
  //           }));
  //         }
  //         let query_arr = gen_query(data);
  //         console.log("query_arr");
  //         console.log(query_arr);
          
  //         for (let i = 0; i < data.length; i++) {
  //           new_card_array.push(
  //             <Card
  //               clicker={() =>
  //                 router.push({ pathname: "/product_pg", query: query_arr[i] })
  //               }
  //               obj={gen_obj(data[i])}
  //               key={data[i].p_uid}
  //             />
  //           );
  //         }

  //         if(new_card_array.length==0)
  //         {
  //           new_card_array.push(
  //             <div style={{width:"700px",justifyContent:"center",display:"flex"}}>No data to show!</div>
  //             )
  //         }
  //         setLoader(false);
  //         setCardsState(new_card_array);
  //       })
  //     )
  //     .catch((err) => {setLoader(false);new_card_array.push(
        
  //       <div style={{width:"700px",justifyContent:"center",display:"flex"}}>No data to show!</div>
  //         )
        
  //         setCardsState(new_card_array);} );
  // }, [newState]);

  useEffect(() => {

    const fetchData = async () => {
            console.log("product fetch");
            let url_fetch = `${apiUrl}/api/products/findByTags`;
            let loc_fetch = `?location=${newState.location}`;
            let cat_fetch = `&category=${newState.category}`;

            if (newState.location == "") {
            loc_fetch = "";
            cat_fetch = "?" + cat_fetch;
            }

            if (newState.category == "") {
            cat_fetch = "";
            }
            url_fetch = url_fetch + loc_fetch + cat_fetch;
            try {
            const response =  await axios(url_fetch) 
            const data = response.data ; 
                
                console.log("printing data");
                console.log(data);
                console.log("entered json method");
                function gen_obj(data) {
                    let id = data.p_uid;
                    let location = data.location;
                    let category = data.category;
                    let product_img_url = data.product_img_url;
                    let description = data.product_description;
                    let company_name = data.company_name;
                    let company_img_url = data.company_img_url;
                    let contractor_id = data.contractor_id;
                    let contractor_name = data.contractor_name;

                    let obj = {
                    id,
                    location,
                    category,
                    product_img_url,
                    description,
                    company_name,
                    company_img_url,
                    contractor_id,
                    contractor_name,
                    };
                    return obj;
                }

                function gen_query(data_arr) {
                    return data_arr.map((x) => ({
                    company_img_url: x.company_img_url,
                    product_img_url: x.product_img_url,
                    description: x.description,
                    contractor_name: x.contractor_name,
                    category: x.category,
                    id: x.p_uid,
                    company_id: x.company_id,
                    contractor_id: x.contractor_id,
                    }));
                }
                let query_arr = gen_query(data);
                console.log("query_arr");
                console.log(query_arr);
                
                for (let i = 0; i < data.length; i++) {
                    new_card_array.push(
                    <Card
                        clicker={() =>
                        router.push({ pathname: "/product_pg", query: query_arr[i] })
                        }
                        obj={gen_obj(data[i])}
                        key={data[i].p_uid}
                    />
                    );
                }

                if(new_card_array.length==0)
                {
                    new_card_array.push(
                    <div style={{width:"700px",justifyContent:"center",display:"flex"}}>No data to show!</div>
                    )
                }
                setLoader(false);
                setCardsState(new_card_array);
            }
            
            catch (err) { 
              console.log(err)
              setLoader(false);new_card_array.push(
                
                <div style={{width:"700px",justifyContent:"center",display:"flex"}}>No data to show!</div>
                )
                
                setCardsState(new_card_array);} 
    }; fetchData() ; 
  }, [newState]);

  let [locationarr, setlocationarr] = React.useState(["Delhi","Mumbai","Pune","Bangalore","Kolkata","Hyderabad","Chennai","Ahmedabad","Surat","Vishakhapatnam","Jaipur"]);

  let [categoryarr, setcategoryarr] = React.useState(["Design Build Firms","Architects and Building Designers","Interior Designers and Decorators","Civil Engineers and Contractors","Home Builders and Construction Companies","Kitchen and Bath Designers","Landscape Architects and Contractors","TileStone and Countertops","Furniture and Accessories","Flooring and Carpet"]);

  const defaultOptionLocation = locationarr[0];
  const defaultOptionCategory = categoryarr[0];

  return (
    <PageTemplate transparentNav={false} outsideApp darkBg={true} noFilter noFooter={true}>
      <div style={{display:"block"}}>
        <Listing_Box />
        <div className={st.container}>
          <div className={st.search_bars}>
            <div className={st.location}>
              <h3 style={{ margin: "1rem 0 0.5rem 0" }}>Location</h3>
              <Dropdown
                options={locationarr}
                onChange={locationHandler}
                value={defaultOptionLocation}
                placeholder="Select an option"
              />
            </div>
            <div className={st.category}>
              <h3 style={{ margin: "1rem 0 0.5rem 0" }}>Category</h3>
              <Dropdown
                options={categoryarr}
                onChange={categoryHandler}
                value={defaultOptionCategory}
                placeholder="Select an option"
              />
            </div>
          </div>

          <div className={st.display_tags}>
            {newState.location !== "" && (
              <div className={st.tag}>
                {newState.location}
                <button className={st.tag_button} onClick={remove_location}>
                  <img src={cross} className={st.img_button} />
                </button>
              </div> 
            )}
            {newState.category !== "" && (
              <div className={st.tag}>
                {newState.category}
                <button className={st.tag_button} onClick={remove_category}>
                  <img src={cross} className={st.img_button} />
                </button>
              </div>
            )}
          </div>
          <div className={st.cards}>{loader==true?<Spinner/>:cardsState}</div>
        </div>
      </div>
      
      {/* <Footer /> */}
    </PageTemplate> 
  );
}

export default App;
