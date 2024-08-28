import TextQuery from "../inputs/textQuery"

const SliderPage = (props)=>{
    const {result, setResult} = props
    return(
        <div className=" bg-slate-400 w-1/3 pl-4">
            <TextQuery result={result} setResult={setResult}/>
        </div>
    )
}
export default SliderPage