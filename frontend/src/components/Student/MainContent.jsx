
const MainContent = ({ selectedTitle }) => {
  return (
    <main className="flex-1 flex items-center justify-center bg-[#f8f9fc] p-4">
      <h1 className="text-3xl font-bold text-[#071B63]">{selectedTitle}</h1>
    </main>
  );
};

export default MainContent;
