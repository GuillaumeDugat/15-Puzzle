"use strict";

function jouer() {
  $.ajax({
    url : "http://127.0.0.1:8000/play",
    data: {},
    dataType : "json",
    type: "GET",
    success : initialisation,
    error : traiteErreur
    });
}

function un_test(reponse) {
    console.log(reponse.test)
}

function initialisation(reponse) {
    $(".grille").replaceWith($("<table>", {id : reponse.id, class : "grille"}));
    for (var i = 0 ; i < reponse.nbr_lignes ; ++i){
        $(".grille").append($("<tr>", {id : "ligne_" + i}));
        for (var j = 0 ; j < reponse.nbr_colonnes ; ++j){
            $("#ligne_" + i).append($("<td>", {id : "case_" + i + "_" + j}));
        };
    };
    $("#nbr_coups").remove()
    $(".grille").after($("<p>", {id : "nbr_coups"}));
    affichage_grille(reponse.grille, reponse.nbr_coups);
}

function traiteErreur(jqXHR, textStatus, errorThrown) {
    alert("Erreur " + errorThrown + " : " + textStatus);
}

function affichage_grille(grille, nbr_coups) {
    const nbr_lignes = grille.length;
    const nbr_colonnes = grille[0].length;
    var k;
    var l;
    for (var i = 0 ; i < nbr_lignes ; ++i){
        for (var j = 0 ; j < nbr_colonnes ; ++j){
            k = ~~(grille[i][j] / nbr_colonnes);
            l = grille[i][j] % nbr_colonnes;
            $("#case_" + i + "_" + j).children().each(function(){$(this).remove()})
            $("#case_" + i + "_" + j).append($("<img>", {src : "Images/image_" + k +"_" + l + ".png", width : "180", height : "180",
            onclick : "deplacement(" + i + ", " + j + ")"}));
        }
    }
    $("img[src='Images/image_0_0.png']").hide();
    $("#nbr_coups").text("Nombre de coups : " + nbr_coups);
}

function deplacement(i, j) {
    var id = $(".grille").attr("id");
    $.ajax({
        url : "http://127.0.0.1:8000/move",
        data: {id : id, i : i, j : j},
        dataType : "json",
        type: "GET",
        success : actualisation,
        error : traiteErreur
        });    
}

function actualisation(reponse) {
    affichage_grille(reponse.grille, reponse.nbr_coups);
    if(reponse.win && !reponse.register) {
        var nom = prompt("Bravo ! Vous venez de gagner. \n Pseudo :");
        var id = $(".grille").attr("id");
        $.ajax({
            url : "http://127.0.0.1:8000/win",
            data: {id : id, nom : nom},
            dataType : "json",
            type: "GET",
            success : victoire,
            error : traiteErreur
            });   
    }
}

function victoire(reponse) {
    console.log("Victory successfully registered");
    actualisation_score();
}

function actualisation_score() {
    $.ajax({
        url : "http://127.0.0.1:8000/score",
        data: {},
        dataType : "json",
        type: "GET",
        success : affiche_score,
        error : traiteErreur
        });      
}

function affiche_score(reponse) {
    $("#score").remove();
    $(document.body).append($("<table>", {id : "score", border : "1px solid black"}));
    if(reponse.res.length != 0 ){
        $("#score").append($("<tr>").html("<th>Pseudo</th> <th>Nombre de coups</th>"));
        var pseudo;
        var nbr_coups;
        for (var i = 0 ; i < reponse.res.length ; ++i){
            pseudo = reponse.res[i][0];
            nbr_coups = reponse.res[i][1];
            $("#score").append($("<tr>").html("<td>" + pseudo + "</th> <td>" + nbr_coups + "</th>"));
        }
    }
}

$(document).ready(actualisation_score)