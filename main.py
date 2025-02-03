function processarCurriculos() {
var pastaId = "PASTA_ID_AQUI"; // ID da pasta do Google Drive onde estão os currículos
var planilhaId = "SUA_PLANILHA_ID_AQUI"; // ID da planilha Google Sheets para salvar os resultados
var keywords = ["Python", "Machine Learning", "SQL", "Gestão de Projetos", "SCRUM", "PostgreSQL"];

var pasta = DriveApp.getFolderById(pastaId);
var arquivos = pasta.getFiles();
var resultados = [];

while (arquivos.hasNext()) {
var arquivo = arquivos.next();
var texto = extrairTextoDoArquivo(arquivo);
var status = classificarTexto(texto, keywords);

resultados.push([arquivo.getName(), status]);
}

salvarNoGoogleSheets(planilhaId, resultados);
Logger.log("Processo concluído! Resultados salvos na planilha.");
}

function extrairTextoDoArquivo(arquivo) {
var tipo = arquivo.getMimeType();
var conteudo = "";

if (tipo === "application/pdf") {
conteudo = extrairTextoPDF(arquivo);
} else if (tipo === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") {
conteudo = extrairTextoDOCX(arquivo);
}

return conteudo;
}

function extrairTextoPDF(arquivo) {
var blob = arquivo.getBlob();
var conteudo = DriveApp.createFile(blob).getAs('text/plain').getDataAsString();
return conteudo || "Erro ao extrair texto do PDF.";
}

function extrairTextoDOCX(arquivo) {
var blob = arquivo.getBlob();
var conteudo = blob.getDataAsString();
return conteudo || "Erro ao extrair texto do DOCX.";
}

function classificarTexto(texto, keywords) {
var count = 0;
keywords.forEach(function(keyword) {
if (texto.toLowerCase().includes(keyword.toLowerCase())) {
count++;
}
});

return count >= 2 ? "BOM" : "RUIM";
}

function salvarNoGoogleSheets(planilhaId, dados) {
var planilha = SpreadsheetApp.openById(planilhaId);
var aba = planilha.getActiveSheet();
aba.getRange(aba.getLastRow() + 1, 1, dados.length, 2).setValues(dados);
}
