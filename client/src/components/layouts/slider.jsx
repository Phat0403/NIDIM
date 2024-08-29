import TextQuery from "../inputs/textQuery"
const SliderPage = (props)=>{
    const { setResult, setLoading} = props
    return(
        <div className="flex bg-slate-400 w-1/3 pl-4">
            <TextQuery  setResult={setResult}  setLoading={setLoading}/>
        </div>
    )
}
export default SliderPage