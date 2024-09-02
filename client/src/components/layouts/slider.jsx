import ImageQuery from "../inputs/imageQuery"
import TextQuery from "../inputs/textQuery"
const SliderPage = (props)=>{
    const { setResult, setLoading} = props
    return(
        <div className="flex flex-col border shadow-[0_0px_30px_-15px_rgba(0,0,0,0.3)] bg-[#EDE8F5]  w-1/3 pl-4 mt-1 rounded-lg ">
            <TextQuery  setResult={setResult}  setLoading={setLoading}/>
            <ImageQuery  setResult={setResult}  setLoading={setLoading} />
        </div>
    )
}
export default SliderPage