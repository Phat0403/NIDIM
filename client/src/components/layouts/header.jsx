
import { useState, useEffect } from "react";

const HeaderPage = (props) => {
  const {result} = props
  const data = (result.length > 0 ? result.slice(0, 100).map((item)=>[item.video, item.frame_idx].join(',')) : []).join('\n')
  const onClickBtn = ()=>{
    console.log(data)
    const blob = new Blob([data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.setAttribute('href', url);
    a.setAttribute('download', 'out.csv'); // Tên file tải về
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }
  return (
    <header className="w-full h-10 bg-[#6a6f90] flex items-center justify-end">
  <button onClick={onClickBtn} className="border mr-4 py-1 bg-red-600 hover:bg-red-500 rounded-md px-2 text-white">Export</button>
</header>

  );
};
export default HeaderPage;
