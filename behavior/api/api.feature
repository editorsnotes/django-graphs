# first line starts the feature
Feature: 4.1.2 LDPR servers must provide an RDF representation for LDPRs
  
  Scenario: Request for a subject representation
    Given an existing subject
     When a GET request is received for the subject
     Then the server provides an RDF representation

