<template>
  <div class="row">
    <div class="col-md-4">
      <div class="profile-work">
        <p>WORK LINK</p>
        <a href="#">Website Link</a><br/>
        <a href="#">Bootsnipp Profile</a><br/>
        <a href="#">Bootply Profile</a>
        <p>SKILLS</p>
        <a href="#">Web Designer</a><br/>
        <a href="#">Web Developer</a><br/>
        <a href="#">WordPress</a><br/>
        <a href="#">WooCommerce</a><br/>
        <a href="#">PHP, .Net</a><br/>
      </div>
    </div>
    <div class="col-md-8">
      <div class="tab-content profile-tab" id="myTabContent">
        <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
          <div class="row">
            <div class="col-md-6">
              <label>User Id</label>
            </div>
            <div class="col-md-6">
              <p>{{ userInfo.id }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>Name</label>
            </div>
            <div class="col-md-6">
              <p>{{ userInfo.username }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>Email</label>
            </div>
            <div class="col-md-6">
              <p>{{ userInfo.email }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>Phone</label>
            </div>
            <div class="col-md-6">
              <p>123 456 7890</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>Profession</label>
            </div>
            <div class="col-md-6">
              <p>Web Developer and Designer</p>
            </div>
          </div>
        </div>
        <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
          <div class="row">
            <div class="col-md-6">
              <label>Experience</label>
            </div>
            <div class="col-md-6">
              <p>Expert</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>Hourly Rate</label>
            </div>
            <div class="col-md-6">
              <p>10$/hr</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>Total Projects</label>
            </div>
            <div class="col-md-6">
              <p>230</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>English Level</label>
            </div>
            <div class="col-md-6">
              <p>Expert</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-6">
              <label>Availability</label>
            </div>
            <div class="col-md-6">
              <p>6 months</p>
            </div>
          </div>
          <div class="row">
            <div class="col-md-12">
              <label>Your Bio</label><br/>
              <p>Your detail description</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import router from "@/router";
import {JWTAuth} from '../../../services/jwt.js';
import axios from "axios";

const baseURL = "http://localhost:8000/api";

const jwtAuth = new JWTAuth('http://localhost:8000/auth/');

export default {
  // mixins: [userInfo],
  components: {
  },
  data() {
    return {
      userInfo: {
        email: '',
        userId: null,
        username: '',
        image: null,
      },
    }
  },
  methods: {
    GoToCreatePost() {
      router.push('profile/createPost');
    },
    async userData() {
      const user = await jwtAuth.getCurrentUser();
      axios.post(`${baseURL}/get-user/`, {
        username: user.username
      })
          .then(response => {
            this.userInfo = response.data;
          })
          .catch(err => {
            console.log(err);
          })
      this.userInfo = user;
      this.userInfo.userId = user.id;
      console.log(user);
    },
    getAbsoluteUrl(relativeUrl) {
      return relativeUrl = 'http://localhost:8000/api' + relativeUrl;
    },

  },
  mounted() {
    this.userData();
  }
}
</script>

<style scoped>

.emp-profile {
  padding: 3%;
  margin-top: 1%;
  margin-bottom: 1%;
  border-radius: 0.5rem;
  background: #fff;
}

.profile-img {
  text-align: center;
}

.profile-img img {
  width: 70%;
  height: 100%;
}

.profile-img .file {
  position: relative;
  overflow: hidden;
  margin-top: -20%;
  width: 70%;
  border: none;
  border-radius: 0;
  font-size: 15px;
  background: #212529b8;
}

.profile-img .file input {
  position: absolute;
  opacity: 0;
  right: 0;
  top: 0;
}

.profile-head h5 {
  color: #333;
}

.profile-head h6 {
  color: #0062cc;
}

.profile-edit-btn {
  border: none;
  border-radius: 1.5rem;
  width: 70%;
  padding: 2%;
  font-weight: 600;
  color: #6c757d;
  cursor: pointer;
}

.proile-rating {
  font-size: 12px;
  color: #818182;
  margin-top: 5%;
}

.proile-rating span {
  color: #495057;
  font-size: 15px;
  font-weight: 600;
}

.profile-head .nav-tabs {
  margin-bottom: 5%;
}

.profile-head .nav-tabs .nav-link {
  font-weight: 600;
  border: none;
}

.profile-head .nav-tabs .nav-link.active {
  border: none;
  border-bottom: 2px solid #0062cc;
}

.profile-work {
  padding: 14%;
  margin-top: -15%;
}

.profile-work p {
  font-size: 12px;
  color: #818182;
  font-weight: 600;
  margin-top: 10%;
}

.profile-work a {
  text-decoration: none;
  color: #495057;
  font-weight: 600;
  font-size: 14px;
}

.profile-work ul {
  list-style: none;
}

.profile-tab label {
  font-weight: 600;
}

.profile-tab p {
  font-weight: 600;
  color: #0062cc;
}

.btn {
  border-radius: 50px;
  font-size: 16px;
}

</style>
