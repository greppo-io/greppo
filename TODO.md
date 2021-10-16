# TODO

## Backend (Py Library)

Comments for the backend code.

* The inputs for the vector data are only the geo-dataframe (required, rest are optional), title, description and colour. The optional params (title, description, color are all given defaults within the library). The zoom, and v-ew center are also calculated in the library. So, the osm and colorbrewer functions can go inside a folder called /utils or so and implemented inside the library.

* Clean the /library folder. You can create the library to now use the greppo word and structure the library that would more resemble the end package.

* Create all the tests in /tests . I will start using these tests for the frontend development as well.

* To keep track of dev requirements and the main requirements, is it an idea to use Poetry? So it will be easier to package.

* End points - API Documentation? Let's start also documenting the end-points for internal reference.

## Frontend (Vue JS)

* Input components. Start with Number input. A change will send a post request. v-input -> v-model -> onChange -> setter -> Mutate -> POST request. Input endpoint? Give specifications to TVS.

* Multipane and pane resizer implementation.

* Responsive design. Establish breakpoints and check at each breakpoint.

* Get status from backend and show error status in the loading modal. 

* Make the data fetch endpoint, point to the open endpoint that it is launched from. Check a vue project with starlette or flask or anything to resolve this. 