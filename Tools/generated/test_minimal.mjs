import { Presentation, PresentationFile } from "file:///C:/Users/leona/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";
const p=Presentation.create({slideSize:{width:1280,height:720}});
p.slides.add();
const pptx=await PresentationFile.exportPptx(p);
await pptx.save("C:/Users/leona/Documents/PL Mathe/Abgabe/test_minimal.pptx");
console.log('ok');
