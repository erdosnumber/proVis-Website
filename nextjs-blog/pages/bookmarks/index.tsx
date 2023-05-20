import React, { useEffect, useState } from "react";
import PageTemplate from "../../components/reusable/template/PageTemplate";
import Card from "../../components/listing_pg/components/card";
import Spinner from "../../components/authModal/components/spinner";
import st from "../../styles/listing_pg/card.module.css";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../redux/reducers";
import config from "config";
import { useRouter } from "next/router.js";

export default function Bookmarks() {
  let [newState, SetState] = React.useState({ location: "", category: "" });
  let [cardsState, setCardsState] = React.useState([]);
  let [loader, setLoader] = React.useState(true);
  const { apiUrl } = config;
  const router = useRouter();

  let new_card_array = [];

  const userId = useSelector((state: RootState) => state.storage.userID);

  useEffect(() => {
    let url_fetch = `${apiUrl}/api/customers/${userId}/bookmarks`; //!maybe wrong url

    // [
    //   {
    //       "cus_uid": 1,
    //       "id": 1,
    //       "product": {
    //           "category": "Architects and Building Designers",
    //           "company_id": "",
    //           "company_img_url": "",
    //           "company_name": "",
    //           "contractor_id": 1,
    //           "contractor_name": "Akshay Verma",
    //           "location": "Delhi",
    //           "p_uid": 1,
    //           "product_description": "The building will have premium quality and luxury amenities and the focus on cutting-edge technology and sustainable design",
    //           "product_img_url": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8YmVhdXRpZnVsJTIwaG91c2V8ZW58MHx8MHx8&w=1000&q=80"
    //       }
    //   },
    // ]

    fetch(url_fetch, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        //Authorization: `Bearer ${jwt}`,
      },
    })
      .then((response) =>
        response.json().then((data) => {
          function gen_obj(e) {
            let data = e.product;
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
              company_img_url: x.product.company_img_url,
              product_img_url: x.product.product_img_url,
              description: x.product.description,
              contractor_name: x.product.contractor_name,
              category: x.product.category,
              id: x.product.p_uid,
              company_id: x.product.company_id,
              contractor_id: x.product.contractor_id,
            }));
          }
          let query_arr = gen_query(data);

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

          if (new_card_array.length == 0) {
            new_card_array.push(<div>No data to show!</div>);
          }
          setLoader(false);
          setCardsState(new_card_array);
        })
      )
      .catch((err) => {
        setLoader(false);
        new_card_array.push(
          <div
            style={{
              width: "700px",
              justifyContent: "center",
              display: "flex",
            }}
          >
            No data to show!
          </div>
        );

        setCardsState(new_card_array);
      });
  }, []);

  return (
    <PageTemplate outsideApp>
      <div className={st.cards} style={{width:"100%", display:"flex",justifyContent:"center",alignItems:"center", flexDirection:"column"}}>
        {loader == true ? <Spinner /> : cardsState}
      </div>
    </PageTemplate>
  );
}
