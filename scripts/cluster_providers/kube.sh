#!/bin/bash -e

function create_cluster(){
   echo "No need to create cluster since kubeconfig is provided externally"
}

function delete_cluster() {
   echo "Deletion can not be performed on external cluster"
}

function get_cluster_auth() {
   echo "export KUBECONFIG=$1"
}
